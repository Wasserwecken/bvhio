import os
import glm
import numpy
import errno
from .bvh import *
from io import TextIOWrapper


def parseLine(file:TextIOWrapper, lineNumber:int) -> tuple[int, list[str], tuple[TextIOWrapper, int, int, str]]:
    lineNumber += 1
    line = file.readline()
    tokens = line.strip().split()
    debugInfo = (file, lineNumber, len(line) - len(line.lstrip()) + len(tokens[0]), line)
    return (lineNumber, tokens, debugInfo)

def read(path:str) -> BVH:
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    result = BVH()
    with open(path, "r") as file:
        line, tokens, debugInfo = parseLine(file, 0)
        if not tokens[0] == 'HIERARCHY' and len(tokens) == 1:
            raise SyntaxError('First line must be only "HIERARCHY"', debugInfo)

        line, tokens, debugInfo = parseLine(file, line)
        if tokens[0] != 'ROOT':
            raise SyntaxError('First Joint must be defined as "ROOT"', debugInfo)
        result.Hierarchy = parseJoint(file, deserializeJointName(tokens, debugInfo))
        calculateBones(result.Hierarchy)

        line, tokens, debugInfo = parseLine(file, line)
        if not tokens[0] == 'MOTION' and len(tokens) == 1:
            raise SyntaxError('After end of hierarchy must follow "MOTION"', debugInfo)

        keyframes = []
        while(True):
            try:
                line, tokens, debugInfo = parseLine(file, line)
                if 'Frames' in tokens[0]:
                    pass
                elif len(tokens) == 3 and tokens[0] == 'Frame':
                    result.FrameTime = deserializeFrameTime(tokens[2:], debugInfo)
                else:
                    deserializeMotion(result.Hierarchy, deserializeKeyframe(tokens, debugInfo))
            except:
                break

        return result

def parseJoint(file:TextIOWrapper, name:str, line:int = 0) -> Joint:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '{' or len(tokens) > 1:
        raise SyntaxError('Joint definition must start with an opening bracket', debugInfo)

    joint = Joint(name)
    joint.Position = deserializeOffset(file, line)
    joint.Channels = deserializeChannles(file, line)

    while(True):
        line, tokens, debugInfo = parseLine(file, line)
        if tokens[0] == 'JOINT':
            joint.append(parseJoint(file, deserializeJointName(tokens, debugInfo), line))
        elif tokens[0] == 'End':
            joint.Tip = deserializeEndSite(file, line)
        elif tokens[0] == '}':
            return joint
        else:
            raise SyntaxError('Joint definition must end with an child joint, end site or closing bracket', debugInfo)

def deserializeJointName(tokens:list[str], debugInfo:tuple[TextIOWrapper, int, int, str]) -> str:
    if not isinstance(tokens, list) and len(tokens) != 2:
        raise SyntaxError('Joint header must be 2-dimensional tuple', debugInfo)
    return tokens[1]

def deserializeOffset(file:TextIOWrapper, line:int) -> glm.vec3:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != 'OFFSET':
        raise SyntaxError('Expected OFFSET definition for joint', debugInfo)
    if not isinstance(tokens, list) or len(tokens[1:]) != 3:
        raise SyntaxError('Offset must be a 3-part tuple', debugInfo)
    try:
        return glm.vec3(list(map(float, tokens[1:])))
    except ValueError:
        raise SyntaxError('Offset must be numerics only', debugInfo)

def deserializeChannles(file:TextIOWrapper, line:int) -> list[str]:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != 'CHANNELS':
        raise SyntaxError('Expected CHANNELS definition for joint', debugInfo)
    if not isinstance(tokens, list) or len(tokens) < 2:
        raise SyntaxError('Channels must be at least a 2-part tuple', debugInfo)
    try:
        channelCount = int(tokens[1])
    except ValueError:
        raise SyntaxError(f'Channel count must be numerical', debugInfo)
    if channelCount != len(tokens[2:]):
        raise SyntaxError(f'Channel count mismatch with labels', debugInfo)
    return tokens[2:]

def deserializeEndSite(file:TextIOWrapper, line:int) -> glm.vec3:
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '{':
        raise SyntaxError('End Site definition must start with an opening bracket', debugInfo)
    result = deserializeOffset(file, line)
    line, tokens, debugInfo = parseLine(file, line)
    if tokens[0] != '}':
        raise SyntaxError('End Site definition must start with an opening bracket', debugInfo)
    return result

def calculateBones(joint:Joint) -> None:
    tipDir = glm.normalize(joint.Tip)
    tipDot = glm.abs(glm.dot(tipDir, glm.vec3(0, 0, 1)))
    tipAxis = glm.vec3(0, 0, 1) if tipDot < 0.9999 else glm.vec3(1, 0, 0)

    joint.Bone.Position = joint.Position
    joint.Bone.Orientation = glm.quatLookAtRH(tipDir, tipAxis)

    for child in joint.Children:
        calculateBones(child)

def deserializeFrameTime(data:list, debugInfo:tuple) -> float:
    if not isinstance(data, list) or len(data) != 1:
        raise SyntaxError('Frame time must be a 1-dimensional tuple', debugInfo)
    try:
        return float(data[0])
    except ValueError:
        raise SyntaxError('Frame time be numerical', debugInfo)

def deserializeKeyframe(data:list, debugInfo:tuple) -> numpy.ndarray:
    try:
        return numpy.array(list(map(float, data)))
    except ValueError:
        raise SyntaxError('Keyframe must be numerics only', debugInfo)

def deserializeMotion(joint:Joint, data:numpy.ndarray, startIndex = 0) -> None:
    position = glm.vec3(joint.Bone.Position)
    orientation = glm.quat()
    for (index, channel) in enumerate(joint.Channels):
        value = data[startIndex + index]
        if 'Xposition' == channel: position.x = value; continue
        if 'Yposition' == channel: position.y = value; continue
        if 'Zposition' == channel: position.z = value; continue
        if 'Xrotation' == channel: orientation = glm.rotate(orientation, glm.radians(value), (1.0, 0.0, 0.0)); continue
        if 'Yrotation' == channel: orientation = glm.rotate(orientation, glm.radians(value), (0.0, 1.0, 0.0)); continue
        if 'Zrotation' == channel: orientation = glm.rotate(orientation, glm.radians(value), (0.0, 0.0, 1.0)); continue
    joint.Keyframes.append(Keyframe(position, orientation))

    joint.Position = position
    joint.Orientation = orientation

    targetOrienation = glm.quat(joint.SpaceWorld) * joint.Bone.Orientation
    w = joint.SpaceWorld * glm.vec4(0,0,0,1)
    x = targetOrienation * glm.vec3(1, 0, 0)
    y = targetOrienation * glm.vec3(0, 1, 0)
    z = targetOrienation * glm.vec3(0, 0, -1)

    for child in joint.Children:
        deserializeMotion(child, data, startIndex + len(joint.Channels))



def write(path:str, bvh:BVH, percision:int = 9) -> None:
    with open(path, "w") as file:
        file.write('HIERARCHY\n')
        writeHierarchy(file, bvh.Hierarchy, 0, True, percision)

        file.write('MOTION\n')
        file.write(f'Frames: {bvh.Frames}\n')
        file.write(f'Frame Time: {bvh.FrameTime}\n')

        for frame in range(bvh.Frames):
            writeMotion(file, bvh.Hierarchy, frame, percision)
            file.write('\n')

def writeHierarchy(file:TextIOWrapper, joint:Joint, indent:int, isFirst:bool, percision:int) -> None:
    offset = joint.Bone.Position
    file.write(f'{" "*indent}{"ROOT" if isFirst else "JOINT"} {joint.Name}\n')
    file.write(f'{" "*indent}{{\n')
    file.write(f'{" "*(indent+1)}OFFSET {round(offset.x, percision)} {round(offset.y ,percision)} {round(offset.z, percision)}\n')
    file.write(f'{" "*(indent+1)}CHANNELS {len(joint.Channels)} {" ".join(joint.Channels)}\n')
    if len(joint.Children) > 0:
        for child in joint.Children:
            writeHierarchy(file, child, indent+1, False, percision)
    else:
        file.write(f'{" "*(indent+1)}End Site\n{" "*(indent+1)}{{\n{" "*(indent+2)}OFFSET 0.0 0.0 0.0\n{" "*(indent+1)}}}\n')
    file.write(f'{" "*indent}}}\n')

def writeMotion(file:TextIOWrapper, joint:Joint, frame:int, percision:int) -> None:
    position = joint.Keyframes[frame].Position
    orientation = joint.Keyframes[frame].Orientation

    rotOrder = ''.join([rot[0] for rot in joint.Channels if rot[1:] == 'rotation'])
    rotMat = glm.transpose(glm.mat3_cast(orientation))
    rotation = glm.degrees(glm.vec3(tr.euler.fromMatTo(rotMat, rotOrder)))

    for channel in joint.Channels:
        if 'Xposition' == channel: file.write(f'{round(position.x, percision)} '); continue
        if 'Yposition' == channel: file.write(f'{round(position.y, percision)} '); continue
        if 'Zposition' == channel: file.write(f'{round(position.z, percision)} '); continue
        if 'Xrotation' == channel: file.write(f'{round(rotation.x, percision)} '); continue
        if 'Yrotation' == channel: file.write(f'{round(rotation.y, percision)} '); continue
        if 'Zrotation' == channel: file.write(f'{round(rotation.z, percision)} '); continue

    for child in joint.Children:
        writeMotion(file, child, frame, percision)
