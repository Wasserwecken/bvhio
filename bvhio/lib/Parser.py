import os
import glm
import numpy
import errno

from io import TextIOWrapper
from SpatialTransform import Euler

from .bvh import *
from .hierarchy import *
from .shared import *

# from shared.Pose import Pose


def parseLine(file: TextIOWrapper, lineNumber: int) -> tuple[int, list[str], tuple[TextIOWrapper, int, int, str]]:
    lineNumber += 1
    line = file.readline()
    tokens = line.strip().split()
    debugInfo = (file, lineNumber, len(line) - len(line.lstrip()) + len(tokens[0]), line)
    return (lineNumber, tokens, debugInfo)


def readAsBVH(path: str) -> BvhContainer:
    """Reads .bvh file as simple structure."""
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
        bvh.Root = parseJoint(file, deserializeJointName(tokens, debugInfo))

        # check for 'MOTION' start
        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'MOTION' or not len(tokens) == 1:
            raise SyntaxError('After end of hierarchy must follow "MOTION"', debugInfo)

        # check for frame count
        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'Frames:' or not len(tokens) == 2:
            raise SyntaxError('First line of "MOTION" section has to be "Frames: X"', debugInfo)
        else:
            bvh.FrameCount = deserializeFrameCount(tokens[1:], debugInfo)

        # check for frame rate
        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'Frame' or not len(tokens) == 3:
            raise SyntaxError('After frame count must follow "Frame Time"', debugInfo)
        else:
            bvh.FrameTime = deserializeFrameTime(tokens[2:], debugInfo)

        # parse motion data
        for _ in range(bvh.FrameCount):
            line, tokens, debugInfo = parseLine(file, line)
            deserializeMotion(bvh.Root, deserializeKeyframe(tokens, debugInfo))

        return bvh


def convertBvhToJoint(pose: RootPose) -> Joint:
    """Convers a simple bvh srtucture to a transform hierarchy."""
    joint = Joint(pose.Name, pose.Offset, pose.getRotation())
    joint.Keyframes = [Pose(f.Position, f.Rotation * joint.RotationLocal) for f in pose.Keyframes]

    for child in pose.Children:
        child = convertBvhToJoint(child)
        for frame in child.Keyframes:
            frame.Position = glm.inverse(joint.RotationLocal) * frame.Position
            frame.Rotation = glm.inverse(joint.RotationLocal) * frame.Rotation
        joint.attach(child, keepPosition=False, keepRotation=False, keepScale=False)
    return joint


def read(path: str) -> Joint:
    """Reads .bvh file as transform hierarchy."""
    return convertBvhToJoint(readAsBVH(path).Root).readPose(0, recursive=True)


def parseJoint(file: TextIOWrapper, name: str, line: int = 0) -> RootPose:
    # check for open bracket
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '{' or len(tokens) > 1:
        raise SyntaxError('Joint definition must start with an opening bracket', debugInfo)

    # create joint and read channels and offeset
    joint = RootPose(name)
    joint.Offset = deserializeOffset(file, line)
    joint.Channels = deserializeChannles(file, line)

    # check for definition end or child joints or end site info
    while (True):
        line, tokens, debugInfo = parseLine(file, line)
        if tokens[0] == 'JOINT':
            joint.Children.append(parseJoint(file, deserializeJointName(tokens, debugInfo), line))
        elif tokens[0] == 'End':
            joint.EndSite = deserializeEndSite(file, line)
        elif tokens[0] == '}':
            break
        else:
            raise SyntaxError('Joint definition must end with an child joint, end site or closing bracket', debugInfo)

    # return deserialized joint root pose
    return joint


def deserializeJointName(tokens: list[str], debugInfo: tuple[TextIOWrapper, int, int, str]) -> str:
    if not isinstance(tokens, list) and len(tokens) != 2:
        raise SyntaxError('Joint header must be 2-dimensional tuple', debugInfo)
    return tokens[1]


def deserializeOffset(file: TextIOWrapper, line: int) -> glm.vec3:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != 'OFFSET':
        raise SyntaxError('Expected OFFSET definition for joint', debugInfo)
    if not isinstance(tokens, list) or len(tokens[1:]) != 3:
        raise SyntaxError('Offset must be a 3-part tuple', debugInfo)
    try:
        return glm.vec3(list(map(float, tokens[1:])))
    except ValueError:
        raise SyntaxError('Offset must be numerics only', debugInfo)


def deserializeChannles(file: TextIOWrapper, line: int) -> list[str]:
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


def deserializeEndSite(file: TextIOWrapper, line: int) -> glm.vec3:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '{':
        raise SyntaxError('End Site definition must start with an opening bracket', debugInfo)
    result = deserializeOffset(file, line)
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '}':
        raise SyntaxError('End Site definition must start with an opening bracket', debugInfo)
    return result


def deserializeFrameTime(data: list, debugInfo: tuple) -> float:
    if not isinstance(data, list) or len(data) != 1:
        raise SyntaxError('Frame time must be a 1-dimensional tuple', debugInfo)
    try:
        return float(data[0])
    except ValueError:
        raise SyntaxError('Frame time be numerical', debugInfo)


def deserializeFrameCount(data: list, debugInfo: tuple) -> float:
    if not isinstance(data, list) or len(data) != 1:
        raise SyntaxError('Frame count must be a 1-dimensional tuple', debugInfo)
    try:
        return int(data[0])
    except ValueError:
        raise SyntaxError('Frame time be numerical', debugInfo)


def deserializeKeyframe(data: list, debugInfo: tuple) -> numpy.ndarray:
    try:
        return numpy.array(list(map(float, data)))
    except ValueError:
        raise SyntaxError('Keyframe must be numerics only', debugInfo)


def deserializeMotion(joint: RootPose, data: numpy.ndarray, index=0) -> int:
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
        index += 1
    joint.Keyframes.append(Pose(position, Euler.toQuatFrom(glm.radians(rotation), rotOrder, False)))

    for child in joint.Children:
        index = deserializeMotion(child, data, index)
    return index
