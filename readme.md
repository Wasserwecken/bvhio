# bvhio
Libary for reading [Biovision .bvh](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html) files and converting the data into a hierarchical spatial structure, as 3D apps would do it.

## Install
```pip install bvhio```

## Features
- Deserialize BVH into hierarchical structure.
- Converts BVH data into proper hierarchical transforms like 3D apps.
- Transforms data is converted to work without base pose.
- Allows reading joint properties in local and world space.
- Space is defined as: Y+ is Up and right handed like openGL
- Transform logic uses the package [spatial-transform](https://github.com/Wasserwecken/spatial-transform)
- Calculations are done with [PyGLM](https://github.com/Zuzu-Typ/PyGLM)

## Examples
### Read, load and show data from a bvh file
```python
import bvhio

# deserialize (https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/Example1.bvh)
bvh = bvhio.read('example.bvh')
print(bvh.Frames)
print(bvh.FrameTime)

# load first pose
bvh.Hierarchy.readPose(0)

# show the world space position of all joints in the current pose
for (joint, index, depth) in bvh.Hierarchy.layout():
    print(joint.pointToWorld((0,0,0)), joint.ForwardWorld, joint.Name)

# OUTPUT:
# 2
# 0.033333
# vec3(         8.03,        35.01,        88.36 ) Hips
# vec3(      8.32964,      40.0387,      89.6891 ) Chest
# vec3(      9.16411,       56.599,      81.1521 ) Neck
# vec3(      10.0571,      58.3157,      76.0571 ) Head
# vec3(      8.02774,      53.6107,      80.5308 ) LeftCollar
# vec3(      2.66686,      55.0047,      80.6263 ) LeftUpArm
# vec3(     -8.11043,      57.0454,       75.859 ) LeftLowArm
# vec3(     -6.00359,      50.1956,      68.9853 ) LeftHand
# vec3(      10.2629,      53.5708,      80.6721 ) RightCollar
# vec3(      16.0524,       55.262,      81.3554 ) RightUpArm
# vec3(      27.7812,      56.5094,      80.5862 ) RightLowArm
# vec3(      28.9073,      64.6527,      73.8156 ) RightHand
# vec3(      4.25561,      34.9653,      89.3799 ) LeftUpLeg
# vec3(     0.900007,      17.2952,      92.9663 ) LeftLowLeg
# vec3(    -0.391914,      9.47834,      108.424 ) LeftFoot
# vec3(      11.8044,      35.0547,      87.3401 ) RightUpLeg
# vec3(      14.8047,       19.916,      78.8176 ) RightLowLeg
# vec3(      17.1327,      4.58867,      86.1275 ) RightFoot
```
