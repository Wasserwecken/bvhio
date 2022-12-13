import bvhio
import numpy
import glm

numpy.set_printoptions(precision=2)
numpy.set_printoptions(suppress=True)

result = bvhio.read('file1.bvh')

# result.Hierarchy.readPose(0)
for (joint, _, _) in result.Hierarchy.layout():
    print(joint.Position, joint.GetEuler(), joint.SpaceWorld * glm.vec4(0,0,0,1), joint.Name)

# result.Hierarchy.applyRotation(True)
# result.Hierarchy.writeOrigin()


result.Hierarchy.readPose(0)
result.Hierarchy.writeBone(True)
bvhio.write('bar.bvh', result)

# result.deserializePose(0)
# foo = numpy.abs(result.serializePose() - result.Motion[0])

# for (i, l) in enumerate(result.Hierarchy.layout(0)):
#     print(f'{l[0].Name}\t {foo[6*i:6*(i+1)]}')

pass
