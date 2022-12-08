import math
import numpy

#https://en.wikipedia.org/wiki/Euler_angles

class euler:
    def fromMatTo(mat3x3:numpy.ndarray, order:str) -> tuple[float, float, float]:
        if order.upper() == 'XYZ': return euler.fromMatToXYZ(mat3x3)
        if order.upper() == 'XZY': return euler.fromMatToXZY(mat3x3)
        if order.upper() == 'YXZ': return euler.fromMatToYXZ(mat3x3)
        if order.upper() == 'YZX': return euler.fromMatToYZX(mat3x3)
        if order.upper() == 'ZXY': return euler.fromMatToZXY(mat3x3)
        if order.upper() == 'ZYX': return euler.fromMatToZYX(mat3x3)

    def fromMatToXZY(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
        return (
            math.atan2(mat3x3[2,1], mat3x3[1,1]),
            math.atan2(mat3x3[0,2], mat3x3[0,0]),
            math.atan2(-mat3x3[0,1], math.sqrt(1 - mat3x3[0,1]**2)),
        )

    def fromMatToXYZ(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
        return (
            math.atan2(-mat3x3[1,2], mat3x3[2,2]),
            math.atan2(mat3x3[0,2], math.sqrt(1 - mat3x3[0,2]**2)),
            math.atan2(-mat3x3[0,1], mat3x3[0,0]),
        )

    def fromMatToYXZ(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
        return (
            math.atan2(-mat3x3[1,2], math.sqrt(1 - mat3x3[1,2]**2)),
            math.atan2(mat3x3[0,2], mat3x3[2,2]),
            math.atan2(mat3x3[1,0], mat3x3[1,1]),
        )

    def fromMatToYZX(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
        return (
            math.atan2(-mat3x3[1,2], mat3x3[1,1]),
            math.atan2(-mat3x3[2,0], mat3x3[0,0]),
            math.atan2(mat3x3[1,0], math.sqrt(1 - mat3x3[1,0]**2)),
        )

    def fromMatToZYX(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
        return (
            math.atan2(mat3x3[2,1], mat3x3[2,2]),
            math.atan2(-mat3x3[2,0], math.sqrt(1 - mat3x3[2,0]**2)),
            math.atan2(mat3x3[1,0], mat3x3[0,0]),
        )

    def fromMatToZXY(mat3x3:numpy.ndarray) -> tuple[float, float, float]:
        return (
            math.atan2(mat3x3[2,1], math.sqrt(1 - mat3x3[2,1]**2)),
            math.atan2(-mat3x3[2,0], mat3x3[2,2]),
            math.atan2(-mat3x3[0,1], mat3x3[1,1]),
        )
