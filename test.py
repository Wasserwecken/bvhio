import bvhio
import numpy

numpy.set_printoptions(precision=2)
numpy.set_printoptions(suppress=True)

bvh = bvhio.read('file2.bvh')

bvh.Hierarchy.readPose(150)
for (joint, index, depth) in bvh.Hierarchy.layout():
    print(joint.pointToWorld((0,0,0)), joint.ForwardWorld, joint.Name)

pass
