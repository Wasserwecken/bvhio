import os
import glm
import numpy
import errno
from .bvh import *
from io import TextIOWrapper


def write(path:str, bvh:BVH, percision:int = 5) -> None:
    bvh.Hierarchy.readOrigin()
    with open(path, "w") as file:
        file.write('HIERARCHY\n')
        writeJoint(file, bvh.Hierarchy, 0, True, percision)

        file.write('MOTION\n')
        file.write(f'Frames: {bvh.Frames}\n')
        file.write(f'Frame Time: {bvh.FrameTime}\n')

        for frame in numpy.round(bvh.Motion, percision):
            stringNumbers = [f'{n}' for n in frame]
            file.write(f'{" ".join(stringNumbers)}\n')

def writeJoint(file:TextIOWrapper, joint:Joint, indent:int, isFirst:bool, percision:int = 9) -> None:
    offset = glm.quat(joint.SpaceParent) * joint.Position

    tab = '  '
    file.write(f'{tab*indent}{"ROOT" if isFirst else "JOINT"} {joint.Name}\n')
    file.write(f'{tab*indent}{{\n')
    file.write(f'{tab*(indent+1)}OFFSET {round(offset.x, percision)} {round(offset.y ,percision)} {round(offset.z, percision)}\n')
    file.write(f'{tab*(indent+1)}CHANNELS {len(joint.Channels)} {" ".join(joint.Channels)}\n')
    if len(joint.Children) > 0:
        for child in joint.Children:
            writeJoint(file, child, indent+1, False, percision)
    else:
        file.write(f'{tab*(indent+1)}End Site\n{tab*(indent+1)}{{\n{tab*(indent+2)}OFFSET 0.0 0.0 0.0\n{tab*(indent+1)}}}\n')
    file.write(f'{tab*indent}}}\n')

def read(path:str) -> BVH:
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    result = BVH()
    with open(path, "r") as file:
        lineNumber = 1
        headline = file.readline().strip()
        if not headline == 'HIERARCHY':
            raise SyntaxError('First line must be "HIERARCHY"', (file, 1, 1, headline))

        currentJoint:Joint = None
        for line in file:
            lineNumber += 1
            tokens = line.strip().split()
            debugInfo = (file, lineNumber, len(line) - len(line.lstrip()) + len(tokens[0]), line)

            if tokens[0] == 'ROOT' or tokens[0] == 'JOINT':
                newJoint = Joint(deserializeJoint(tokens[1:], debugInfo))
                if currentJoint is not None:
                    currentJoint.append(newJoint)
                currentJoint = newJoint
                if not file.readline().strip() == '{':
                    raise SyntaxError('Joint header must follow a "{" line', debugInfo)

            elif tokens[0] == 'OFFSET':
                currentJoint.Position = glm.vec3(deserializeOffset(tokens[1:], debugInfo))
                currentJoint.Origin = [currentJoint.Position, glm.quat()]

            elif tokens[0] == 'CHANNELS':
                currentJoint.Channels = deserializeChannles(tokens[1:], debugInfo)

            elif tokens[0] == 'End':
                while file.readline().strip() != '}':
                    pass

            elif tokens[0] == '}':
                if currentJoint is None:
                    raise SyntaxError('Root joint is already closed', debugInfo)
                if currentJoint.Parent is None:
                    result.Hierarchy = currentJoint
                    break
                else:
                    currentJoint = currentJoint.Parent

        lineNumber += 1
        motionLine = file.readline().strip()
        if not motionLine == 'MOTION':
            raise SyntaxError('After end of hierarchy must follow "MOTION"', (file, lineNumber, 1, motionLine))

        keyframes = []
        for line in file:
            lineNumber += 1
            tokens = line.strip().split()
            debugInfo = (file, lineNumber, len(line) - len(line.lstrip()) + len(tokens[0]), line)

            if 'Frames' in tokens[0]:
                pass
            elif len(tokens) == 3 and tokens[0] == 'Frame':
                result.FrameTime = deserializeFrameTime(tokens[2:], debugInfo)
            else:
                keyframes.append(deserializeKeyframe(tokens, debugInfo))

        motion = numpy.array(keyframes)
        for (joint, start, end) in result.Hierarchy.layout():
            joint.deserializeMotion(motion[:, start:end])

        return result


def deserializeJoint(data:list, debugInfo:tuple) -> str:
    if not isinstance(data, list):
        raise SyntaxError('Joint data must be 1-dimensional tuple', debugInfo)
    return data[0]

def deserializeChannles(data:list, debugInfo:tuple) -> list[str]:
    if not isinstance(data, list) or len(data) < 1:
        raise SyntaxError('Channels must be at least a 1-dimensional tuple', debugInfo)
    try:
        data[0] = int(data[0])
    except ValueError:
        raise SyntaxError(f'Channel count must be numerical', debugInfo)
    if not data[0] == len(data) - 1:
        raise SyntaxError(f'Channel count mismatch with labels', debugInfo)
    return data[1:]

def deserializeOffset(data:list, debugInfo:tuple) -> numpy.ndarray:
    if not isinstance(data, list) or len(data) != 3:
        raise SyntaxError('Offset must be a 3-dimensional tuple', debugInfo)
    try:
        return numpy.array(list(map(float, data)))
    except ValueError:
        raise SyntaxError('Offset must be numerics only', debugInfo)

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
