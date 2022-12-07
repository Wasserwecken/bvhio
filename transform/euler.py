import math
import numpy

#https://en.wikipedia.org/wiki/Euler_angles

def to(mat3x3:numpy.ndarray, order:str) -> tuple[float, float, float]:
    if mat3x3[1,1] == 0: mat3x3[1,1] = 1
    if mat3x3[2,2] == 0: mat3x3[2,2] = 1
    if order.upper() == 'XYZ': return toXYZ(mat3x3)
    if order.upper() == 'XZY': return toXZY(mat3x3)
    if order.upper() == 'YXZ': return toYXZ(mat3x3)
    if order.upper() == 'YZX': return toYZX(mat3x3)
    if order.upper() == 'ZXY': return toZXY(mat3x3)
    if order.upper() == 'ZYX': return toZYX(mat3x3)

def toXZY(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
    return (
        math.atan(mat3x3[2,1] / mat3x3[1,1]),                       # X
        math.atan(mat3x3[0,2] / mat3x3[0,0]),                       # Z
        math.atan(-mat3x3[0,1] / math.sqrt(1 - mat3x3[0,1]**2)),    # Y
    )

def toXYZ(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
    return (
        math.atan(-mat3x3[1,2] / mat3x3[2,2]),                     # X
        math.atan(mat3x3[0,2] / math.sqrt(1 - mat3x3[0,2]**2)),    # Y
        math.atan(-mat3x3[0,1] / mat3x3[0,0]),                     # Z
    )

def toYXZ(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
    return (
        math.atan(-mat3x3[1,2] / math.sqrt(1 - mat3x3[1,2]**2)),    # Y
        math.atan(mat3x3[0,2] / mat3x3[2,2]),                       # X
        math.atan(mat3x3[1,0] / mat3x3[1,1]),                       # Z
    )

def toYZX(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
    return (
        math.atan(-mat3x3[1,2] / mat3x3[1,1]),                      # Z
        math.atan(-mat3x3[2,0] / mat3x3[0,0]),                      # X
        math.atan(mat3x3[1,0] / math.sqrt(1 - mat3x3[1,0]**2)),     # Y
    )

def toZYX(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
    return (
        math.atan(mat3x3[2,1] / mat3x3[2,2]),                       # Z
        math.atan(-mat3x3[2,0] / math.sqrt(1 - mat3x3[2,0]**2)),    # Y
        math.atan(mat3x3[1,0] / mat3x3[0,0]),                       # X
    )

def toZXY(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
    return (
        math.atan(mat3x3[2,1] / math.sqrt(1 - mat3x3[2,1]**2)),     # Y
        math.atan(-mat3x3[2,0] / mat3x3[2,2]),                      # Z
        math.atan(-mat3x3[0,1] / mat3x3[1,1]),                      # X
    )
