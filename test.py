import bvhio
import numpy

numpy.set_printoptions(precision=2)
numpy.set_printoptions(suppress=True)

result = bvhio.read('file2.bvh')
# result.Hierarchy.readPose(0)

for (joint, _, _) in result.Hierarchy.layout():
    print(joint.Position, joint.Orientation, joint.GetEuler(), joint.Name)

# result.Hierarchy.applyRotation(True)
# result.Hierarchy.writeOrigin()


bvhio.write('bar.bvh', result)

# result.deserializePose(0)
# foo = numpy.abs(result.serializePose() - result.Motion[0])

# for (i, l) in enumerate(result.Hierarchy.layout(0)):
#     print(f'{l[0].Name}\t {foo[6*i:6*(i+1)]}')

pass
