import bvhio
import numpy
import glm

numpy.set_printoptions(precision=2)
numpy.set_printoptions(suppress=True)

bvh = bvhio.read('file1.bvh')

bvh.Hierarchy.readPose(0)
for joint in bvh.Hierarchy.layout():
    print(joint.Position, joint.pointToWorld((0,0,0)), joint.Name)

pass
