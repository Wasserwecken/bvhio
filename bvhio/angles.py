import math
import glm

#https://en.wikipedia.org/wiki/Euler_angles

def mat3ToEulerXZY(mat:glm.mat3) -> glm.vec3:
    return glm.vec3(
        math.atan(mat[2,1] / mat[1,1]),
        math.atan(-mat[0,1] / math.sqrt(1 - mat[0,1]**2)),
        math.atan(-mat[0,2] / mat[0,0])
    ).xzy

def mat3ToEulerXYZ(mat:glm.mat3) -> glm.vec3:
    return glm.vec3(
        math.atan(mat[1,2] / mat[2,2]),
        math.atan(-mat[0,2] / math.sqrt(1 - mat[0,2]**2)),
        math.atan(-mat[0,1] / mat[0,0])
    ).xyz

def mat3ToEulerYXZ(mat:glm.mat3) -> glm.vec3:
    return glm.vec3(
        math.atan(mat[0,2] / mat[2,2]),
        math.atan(-mat[1,2] / math.sqrt(1 - mat[1,2]**2)),
        math.atan(-mat[1,0] / mat[1,1])
    ).yxz

def mat3ToEulerYZX(mat:glm.mat3) -> glm.vec3:
    return glm.vec3(
        math.atan(mat[2,0] / mat[0,0]),
        math.atan(-mat[1,0] / math.sqrt(1 - mat[1,0]**2)),
        math.atan(-mat[1,2] / mat[1,1])
    ).zxy

def mat3ToEulerZYX(mat:glm.mat3) -> glm.vec3:
    return glm.vec3(
        math.atan(mat[1,0] / mat[0,0]),
        math.atan(-mat[2,0] / math.sqrt(1 - mat[2,0]**2)),
        math.atan(-mat[2,1] / mat[2,2])
    ).zxy

def mat3ToEulerZXY(mat:glm.mat3) -> glm.vec3:
    return glm.vec3(
        math.atan(-mat[0,1] / mat[1,1]),
        math.atan(mat[2,1] / math.sqrt(1 - mat[2,1]**2)),
        math.atan(-mat[2,0] / mat[2,2])
    ).yzx
