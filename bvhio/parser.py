from io import TextIOWrapper
import os
import errno

from .bvh import *

def deserialize(path:str) -> BVH:
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
                newJoint = Joint(currentJoint, deserializeJoint(tokens[1:], debugInfo))

                if not currentJoint:
                    currentJoint = newJoint
                elif (not currentJoint.Children):
                    currentJoint.Children = [newJoint]
                else:
                    currentJoint.Children.append(newJoint)
                currentJoint = newJoint

                if not file.readline().strip() == '{':
                    raise SyntaxError('Joint header must follow a "{" line', debugInfo)

            elif tokens[0] == 'OFFSET':
                currentJoint.Offset = deserializeOffset(tokens[1:], debugInfo)

            elif tokens[0] == 'CHANNELS':
                currentJoint.Channels = deserializeChannles(tokens[1:], debugInfo)

            elif tokens[0] == 'End':
                while file.readline().strip() != '}':
                    pass

            elif tokens[0] == '}':
                if not currentJoint:
                    raise SyntaxError('Root joint is already closed', debugInfo)
                currentJoint = currentJoint.Parent


def deserializeJoint(data:list, debugInfo:tuple) -> str:
    if not isinstance(data, list):
        raise SyntaxError('Joint data must be 1-dimensional tuple', debugInfo)
    return data[0]

def deserializeChannles(data:list, debugInfo:tuple) -> list[str]:
    if not isinstance(data, list):
        raise SyntaxError('Channels must be at least a 1-dimensional tuple', debugInfo)
    if not int(data[0]) == len(data) - 1:
        raise SyntaxError(f'Channel count mismatch with labels', debugInfo)
    return data[1:]

def deserializeOffset(data:list, debugInfo:tuple) -> numpy.ndarray:
    if not isinstance(data, list) or len(data) != 3:
        raise SyntaxError('Offset must be a 3-dimensional tuple', debugInfo)
    data = list(map(float, data))
    if not all([isinstance(item, float) for item in data]):
        raise SyntaxError('Offset must be numerics only', debugInfo)
    return numpy.array(data)
