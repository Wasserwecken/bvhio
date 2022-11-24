import bvhio
import glm

result = bvhio.deserialize('foo.bvh')
print(result.Hierarchy.indicies())
pass

# integrate GLM
# why? -> see following

# add joints
# remove joints
# why? -> Add root, remove root

# swizzle hierarchy
# write BVH
# why? -> some do legs first, some do right first, standarize hierarchy

# scale
# why? -> lower values may be better for NN

