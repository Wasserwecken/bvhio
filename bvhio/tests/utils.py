import glm
import math
import random

deltaPosition = 1e-05
deltaRotation = 1e-05
deltaScale = 1e-05
randomSamples = 10000


def randomPosition():
    return glm.vec3(random.random(), random.random(), random.random()) * 2 - 1

def randomDirection():
    result = glm.vec3(random.random(), random.random(), random.random())
    theta = result.x * math.pi * 2.0
    phi = math.acos((2.0 * result.y) - 1.0)
    r = pow(result.z, 1/3)

    result.x = r * math.sin(phi) * math.cos(theta)
    result.y = r * math.sin(phi) * math.sin(theta)
    result.z = r * math.cos(phi)

    return glm.normalize(result)

def randomRotation():
    return glm.normalize(glm.quatLookAt(randomDirection(), (0,1,0)))

def randomScale():
    return (glm.vec3(random.random(), random.random(), random.random()) + 0.01) * \
         glm.vec3(-1 if random.random()<0.5 else 1, -1 if random.random()<0.5 else 1, -1 if random.random()<0.5 else 1)


def deviationPosition(a:glm.vec3, b:glm.vec3):
    return glm.l1Norm(a - b)

def deviationQuaternion(a:glm.quat, b:glm.quat):
    return sum([abs(d) for d in (a - b).to_list()])

def deviationScale(a:glm.vec3, b:glm.vec3):
    return glm.l1Norm(a - b)
