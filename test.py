import bvhio
import numpy

numpy.set_printoptions(precision=2)
numpy.set_printoptions(suppress=True)

bvh = bvhio.read('file1.bvh')

bvh.Hierarchy.readPose(250)
for joint in bvh.Hierarchy.layout():
    print(joint.pointToWorld((0,0,0)), joint.ForwardWorld, joint.RightWorld, joint.UpWorld, joint.Name)

pass
