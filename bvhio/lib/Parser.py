import os
import glm
import numpy
import errno

from io import TextIOWrapper
from SpatialTransform import Euler, Pose, Transform

from .bvh import *
from .hierarchy import *


def parseLine(file: TextIOWrapper, lineNumber: int) -> tuple[int, list[str], tuple[TextIOWrapper, int, int, str]]:
    lineNumber += 1
    line = file.readline()
    tokens = line.strip().split()
    debugInfo = (file, lineNumber, len(line) - len(line.lstrip()) + len(tokens[0]), line)
    return (lineNumber, tokens, debugInfo)


def readAsBvh(path: str) -> BvhContainer:
    """Deserialize .bvh file into a simple structure."""
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    bvh = BvhContainer()
    with open(path, "r") as file:
        # check for 'HIERARCHY' start
        line, tokens, debugInfo = parseLine(file, 0)
        if not tokens[0] == 'HIERARCHY' and len(tokens) == 1:
            raise SyntaxError('First line must be only "HIERARCHY"', debugInfo)

        # parse joints recursivly
        line, tokens, debugInfo = parseLine(file, line)
        if tokens[0] != 'ROOT':
            raise SyntaxError('First Joint must be defined as "ROOT"', debugInfo)
        bvh.Root = _parseJoint(file, _deserializeJointName(tokens, debugInfo))

        # check for 'MOTION' start
        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'MOTION' or not len(tokens) == 1:
            raise SyntaxError('After end of hierarchy must follow "MOTION"', debugInfo)

        # check for frame count
        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'Frames:' or not len(tokens) == 2:
            raise SyntaxError('First line of "MOTION" section has to be "Frames: X"', debugInfo)
        else:
            bvh.FrameCount = _deserializeFrameCount(tokens[1:], debugInfo)

        # check for frame rate
        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'Frame' or not len(tokens) == 3:
            raise SyntaxError('After frame count must follow "Frame Time"', debugInfo)
        else:
            bvh.FrameTime = _deserializeFrameTime(tokens[2:], debugInfo)

        # parse motion data
        for _ in range(bvh.FrameCount):
            line, tokens, debugInfo = parseLine(file, line)
            _deserializeMotion(bvh.Root, _deserializeKeyframe(tokens, debugInfo))

        return bvh


def convertBvhToHierarchy(bvh: BvhJoint) -> Joint:
    """Converts a deserialized bvh structure into a joint hierarchy."""
    # copy data into a joint
    restPose = Transform(name='RestPose', position=bvh.Offset, rotation=bvh.getRotation())
    joint = Joint(bvh.Name, restPose=restPose)
    for frame, key in enumerate(bvh.Keyframes):
        joint.setKeyframe(frame, Transform.fromPose(key), keep=None)

    # correct bvh keyframe data
    for frame, key in joint.Keyframes:
        # project offset into rest pose because it is given as overwrite and does not include the rest pose rotation.
        key.Position = joint.RestPose.SpaceInverse * key.Position

        # the rotation is already given as difference, but the multiplication order is switched.
        key.Rotation = key.Rotation * joint.RestPose.Rotation
        key.Rotation = (glm.inverse(joint.RestPose.Rotation) * key.Rotation)

    for child in bvh.Children:
        # correct the rest pose, because its given without the parents rest pose rotation.
        childJoint = convertBvhToHierarchy(child)
        childJoint.RestPose.Position = glm.inverse(joint.RestPose.Rotation) * childJoint.RestPose.Position
        childJoint.RestPose.Rotation = glm.inverse(joint.RestPose.Rotation) * childJoint.RestPose.Rotation
        joint.attach(childJoint, keep=None)

    return joint


def convertHierarchyToBvh(joint: Joint, frames: int, worldSpace: Pose = Pose()) -> BvhJoint:
    """Converts a joint structure into a deseralized bvh structure."""
    bvh = BvhJoint(joint.Name)
    bvh.Offset = worldSpace.Space * joint.RestPose.Position
    bvh.EndSite = (worldSpace.Space * (0, 1, 0)) * glm.length(joint.RestPose.Position) * 0.3
    bvh.Keyframes = [joint.getKeyframe(frame).toPose(worldSpace=False) for frame in range(frames)]

    worldSpace.Rotation = worldSpace.Rotation * joint.RestPose.Rotation
    worldSpace.Scale = worldSpace.Scale * joint.RestPose.Scale

    if 1e-02 < glm.l1Norm(sum([glm.abs(pose.Position) for pose in bvh.Keyframes])):
        bvh.Channels.extend(['Xposition', 'Yposition', 'Zposition'])

    if 1e-02 < (sum([sum([abs(d) for d in (pose.Rotation - glm.quat()).to_list()]) for pose in bvh.Keyframes])):
        bvh.Channels.extend(['Zrotation', 'Xrotation', 'Yrotation'])

    # convert data to bvh
    for key in bvh.Keyframes:
        key.Position = bvh.Offset + (worldSpace.Space * key.Position)
        key.Rotation = worldSpace.Rotation * key.Rotation
        key.Rotation = (key.Rotation * glm.inverse(worldSpace.Rotation))

    # add children
    for child in joint.Children:
        childBvh = convertHierarchyToBvh(child, frames, worldSpace.duplicate())
        bvh.Children.append(childBvh)

    return bvh


def readAsHierarchy(path: str) -> Joint:
    """Deserialize a .bvh file into a joint hierarchy."""
    return convertBvhToHierarchy(readAsBvh(path).Root).loadRestPose(recursive=True)


def _parseJoint(file: TextIOWrapper, name: str, line: int = 0) -> BvhJoint:
    # check for open bracket
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '{' or len(tokens) > 1:
        raise SyntaxError('Joint definition must start with an opening bracket', debugInfo)

    # create joint and read channels and offeset
    joint = BvhJoint(name)
    joint.Offset = _deserializeOffset(file, line)
    joint.Channels = _deserializeChannles(file, line)

    # check for definition end or child joints or end site info
    while (True):
        line, tokens, debugInfo = parseLine(file, line)
        if tokens[0] == 'JOINT':
            joint.Children.append(_parseJoint(file, _deserializeJointName(tokens, debugInfo), line))
        elif tokens[0] == 'End':
            joint.EndSite = _deserializeEndSite(file, line)
        elif tokens[0] == '}':
            break
        else:
            raise SyntaxError('Joint definition must end with an child joint, end site or closing bracket', debugInfo)

    # return deserialized joint root pose
    return joint


def _deserializeJointName(tokens: list[str], debugInfo: tuple[TextIOWrapper, int, int, str]) -> str:
    if not isinstance(tokens, list) and len(tokens) != 2:
        raise SyntaxError('Joint header must be 2-dimensional tuple', debugInfo)
    return tokens[1]


def _deserializeOffset(file: TextIOWrapper, line: int) -> glm.vec3:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != 'OFFSET':
        raise SyntaxError('Expected OFFSET definition for joint', debugInfo)
    if not isinstance(tokens, list) or len(tokens[1:]) != 3:
        raise SyntaxError('Offset must be a 3-part tuple', debugInfo)
    try:
        return glm.vec3(list(map(float, tokens[1:])))
    except ValueError:
        raise SyntaxError('Offset must be numerics only', debugInfo)


def _deserializeChannles(file: TextIOWrapper, line: int) -> list[str]:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != 'CHANNELS':
        raise SyntaxError('Expected CHANNELS definition for joint', debugInfo)
    if not isinstance(tokens, list) or len(tokens) < 2:
        raise SyntaxError('Channels must be at least a 2-part tuple', debugInfo)
    try:
        channelCount = int(tokens[1])
    except ValueError:
        raise SyntaxError('Channel count must be numerical', debugInfo)
    if channelCount != len(tokens[2:]):
        raise SyntaxError('Channel count mismatch with labels', debugInfo)
    return tokens[2:]


def _deserializeEndSite(file: TextIOWrapper, line: int) -> glm.vec3:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '{':
        raise SyntaxError('End Site definition must start with an opening bracket', debugInfo)
    result = _deserializeOffset(file, line)
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '}':
        raise SyntaxError('End Site definition must start with an opening bracket', debugInfo)
    return result


def _deserializeFrameTime(data: list, debugInfo: tuple) -> float:
    if not isinstance(data, list) or len(data) != 1:
        raise SyntaxError('Frame time must be a 1-dimensional tuple', debugInfo)
    try:
        return float(data[0])
    except ValueError:
        raise SyntaxError('Frame time be numerical', debugInfo)


def _deserializeFrameCount(data: list, debugInfo: tuple) -> float:
    if not isinstance(data, list) or len(data) != 1:
        raise SyntaxError('Frame count must be a 1-dimensional tuple', debugInfo)
    try:
        return int(data[0])
    except ValueError:
        raise SyntaxError('Frame time be numerical', debugInfo)


def _deserializeKeyframe(data: list, debugInfo: tuple) -> numpy.ndarray:
    try:
        return numpy.array(list(map(float, data)))
    except ValueError:
        raise SyntaxError('Keyframe must be numerics only', debugInfo)


def _deserializeMotion(joint: BvhJoint, data: numpy.ndarray, index=0) -> int:
    position = glm.vec3(joint.Offset)
    rotation = glm.vec3(0)
    rotOrder = ''

    for channel in joint.Channels:
        if 'Xposition' == channel: position.x = data[index]
        elif 'Yposition' == channel: position.y = data[index]
        elif 'Zposition' == channel: position.z = data[index]
        elif 'Xrotation' == channel: rotation.x = data[index]; rotOrder += 'X'
        elif 'Yrotation' == channel: rotation.y = data[index]; rotOrder += 'Y'
        elif 'Zrotation' == channel: rotation.z = data[index]; rotOrder += 'Z'
        else: index -= 1
        index += 1

    rotation = Euler.toQuatFrom(glm.radians(rotation), order=rotOrder, extrinsic=False)
    joint.Keyframes.append(Pose(position, rotation))

    for child in joint.Children:
        index = _deserializeMotion(child, data, index)
    return index


def writeBvh(path: str, bvh: BvhContainer, percision: int = 9) -> None:
    with open(path, "w") as file:
        file.write('HIERARCHY\n')
        writeJoint(file, bvh.Root, 0, True, percision)

        file.write('MOTION\n')
        file.write(f'Frames: {bvh.FrameCount}\n')
        file.write(f'Frame Time: {bvh.FrameTime}\n')

        for frame in range(bvh.FrameCount):
            writeMotion(file, bvh.Root, frame, percision)
            file.write('\n')


def writeHierarchy(path: str, root: Joint, frameTime: float, frames: int = None, percision: int = 9) -> None:
    """Creates an .bvh file from the given hierarchy.
    - frameTime defines the FPS
    - IF frames is None -> THe whole animation is written.
    - If frames is set -> The Animation is written from frame 0 to frame.
    - percision limits the percision of floating numbers be written.
    - Data will be overwritten if the file already exists"""
    frames = (root.getKeyframeRange()[1] + 1) if frames is None else frames
    container = BvhContainer(convertHierarchyToBvh(root, frames + 1), frames, frameTime)
    writeBvh(path, container, percision)


def writeJoint(file: TextIOWrapper, joint: BvhJoint, indent: int, isFirst: bool, percision: int) -> None:
    file.write(f'{"  "*indent}{"ROOT" if isFirst else "JOINT"} {joint.Name}\n')
    file.write(f'{"  "*indent}{{\n')
    file.write(f'{"  "*(indent+1)}OFFSET ')
    file.write(f'{round(joint.Offset.x, percision)} ')
    file.write(f'{round(joint.Offset.y, percision)} ')
    file.write(f'{round(joint.Offset.z, percision)}\n')
    file.write(f'{"  "*(indent+1)}CHANNELS {len(joint.Channels)} {" ".join(joint.Channels)}\n')
    if len(joint.Children) > 0:
        for child in joint.Children:
            writeJoint(file, child, indent + 1, False, percision)
    else:
        file.write(f'{"  "*(indent+1)}End Site\n')
        file.write(f'{"  "*(indent+1)}{{\n')
        file.write(f'{"  "*(indent+2)}OFFSET ')
        file.write(f'{round(joint.EndSite.x, percision)} ')
        file.write(f'{round(joint.EndSite.y, percision)} ')
        file.write(f'{round(joint.EndSite.z, percision)}\n')
        file.write(f'{"  "*(indent+1)}}}\n')
    file.write(f'{"  "*indent}}}\n')


def writeMotion(file: TextIOWrapper, joint: BvhJoint, frame: int, percision: int) -> None:
    rotOrder = ''.join([rot[0] for rot in joint.Channels if rot[1:] == 'rotation'])
    if 'Z' not in rotOrder: rotOrder += 'Z'
    if 'X' not in rotOrder: rotOrder += 'X'
    if 'Y' not in rotOrder: rotOrder += 'Y'

    rotation = joint.Keyframes[frame].getEuler(rotOrder, extrinsic=False)
    position = joint.Keyframes[frame].Position

    for channel in joint.Channels:
        if 'Xposition' == channel: file.write(f'{round(position.x, percision)} '); continue
        if 'Yposition' == channel: file.write(f'{round(position.y, percision)} '); continue
        if 'Zposition' == channel: file.write(f'{round(position.z, percision)} '); continue
        if 'Xrotation' == channel: file.write(f'{round(rotation.x, percision)} '); continue
        if 'Yrotation' == channel: file.write(f'{round(rotation.y, percision)} '); continue
        if 'Zrotation' == channel: file.write(f'{round(rotation.z, percision)} '); continue

    for child in joint.Children:
        writeMotion(file, child, frame, percision)
