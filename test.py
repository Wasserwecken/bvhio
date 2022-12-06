import bvhio
import numpy

numpy.set_printoptions(precision=2)
numpy.set_printoptions(suppress=True)

result = bvhio.read('file2.bvh')

for (joint, _, _) in result.readPose(0).layout():
    print(joint.Position, joint.Euler, joint.Name)

print('#####')
for frame in range(0, 10, 1):
    print(result.readPose(frame).Children[0].Position, end='')
    print(result.readPose(frame).Children[0].Euler, end='')
    print('')

result.setAsHierarchy(result.readPose(0))
bvhio.write('bar.bvh', result)

# result.deserializePose(0)
# foo = numpy.abs(result.serializePose() - result.Motion[0])

# for (i, l) in enumerate(result.Hierarchy.layout(0)):
#     print(f'{l[0].Name}\t {foo[6*i:6*(i+1)]}')

pass
