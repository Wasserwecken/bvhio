# bvhio
Libary for reading [Biovision .bvh](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html) files and converting the data into a hierarchical spatial structure, as 3D apps would do it.

This package is created for my master thesis and aims about integrety but not performance. For the most of the calculations the package [PyGLM](https://github.com/Zuzu-Typ/PyGLM) is used.
## Install
``` batch
pip install bvhio
 ```

## Features
- Deserialize BVH into hierarchical structure.
- Converts BVH data into proper hierarchical transforms like 3D apps.
- Keeps deserialized BVH data.
- Transforms data is converted to work without base pose.
- Allows reading joint properties in local and world space.
- Space is defined as: Y+ is Up and right handed like openGL.
- Transform logic uses the package [spatial-transform](https://github.com/Wasserwecken/spatial-transform)
- Calculations are done with [PyGLM](https://github.com/Zuzu-Typ/PyGLM)
- Python
    - Every method is documented in code with docstrings
    - Every method has type hinting

## Examples
### Read bvh file
```python
import bvhio

bvh = bvhio.read('example.bvh')
print(f'Frames: {bvh.Frames}')
print(f'Frame time: {bvh.FrameTime}')
bvh.Hierarchy.printTree()

# Frames: 2
# Frame time: 0.033333
# Hips
# +- Chest
# |  +- Neck
# |  |  +- Head
# |  +- LeftCollar
# |  |  +- LeftUpArm
# |  |     +- LeftLowArm
# |  |        +- LeftHand
# |  +- RightCollar
# |     +- RightUpArm
# |        +- RightLowArm
# |           +- RightHand
# +- LeftUpLeg
# |  +- LeftLowLeg
# |     +- LeftFoot
# +- RightUpLeg
#    +- RightLowLeg
#       +- RightFoot
```

### bvhio properties and methods
```python
bvh.Frames # Count of keyframes in the bvh
bvh.FrameTime # Time per pose
bvh.Hierarchy # Root joint of the skeleton definition.

# lists all joints attached to the root and their childrens
bvh.Hierarchy.layout()
# Defines the base pose with the hierarchical joint data, including calculated bone Rotation
bvh.Hierarchy.DataBVH
# this is this is the original motion data, rotations are converted to quaternions
bvh.Hierarchy.DataBVH.Keyframes

# motion data converted to pure local space. Independed of the base pose.
bvh.Hierarchy.Keyframes
# updates the transform and all its children to the given pose number.
bvh.Hierarchy.readPose(0)
# updates the motion data to change the keyframe permanently. Tis does NOT update the original BVH data!
bvh.Hierarchy.writePose(0)
```

### Read the hierarchy
```python
# Hierarchy is positioned and aligned by the keyframe
bvh.Hierarchy.readPose(0)

# scale root bone to have the value roughly match meters.
# the root position has to be updated to the scale too!
bvh.Hierarchy.Scale = (0.02, 0.02, 0.02)
bvh.Hierarchy.Position *= bvh.Hierarchy.Scale

# get world space position of all joints
print('Joint positions in world space:')
for joint, index, depth in bvh.Hierarchy.layout():
    print(f'{joint.pointToWorld((0,0,0))} {joint.Name}')

# Joint positions in world space:
# vec3(       0.1606,       0.7002,       1.7672 ) Hips
# vec3(     0.166593,     0.800774,      1.79378 ) Chest
# vec3(     0.183282,      1.13198,      1.62304 ) Neck
# vec3(     0.201143,      1.16631,      1.52114 ) Head
# vec3(     0.160555,      1.07221,      1.61062 ) LeftCollar
# vec3(    0.0533372,      1.10009,      1.61253 ) LeftUpArm
# vec3(    -0.162209,      1.14091,      1.51718 ) LeftLowArm
# vec3(    -0.120072,      1.00391,      1.37971 ) LeftHand
# vec3(     0.205259,      1.07142,      1.61344 ) RightCollar
# vec3(     0.321048,      1.10524,      1.62711 ) RightUpArm
# vec3(     0.555624,      1.13019,      1.61172 ) RightLowArm
# vec3(     0.578145,      1.29305,      1.47631 ) RightHand
# vec3(    0.0851123,     0.699307,       1.7876 ) LeftUpLeg
# vec3(    0.0180001,     0.345904,      1.85933 ) LeftLowLeg
# vec3(  -0.00783825,     0.189567,      2.16848 ) LeftFoot
# vec3(     0.236088,     0.701093,       1.7468 ) RightUpLeg
# vec3(     0.296095,     0.398319,      1.57635 ) RightLowLeg
# vec3(     0.342655,    0.0917735,      1.72255 ) RightFoot
```

### Read joints
```python
# read data for a single joint
arm = bvh.Hierarchy.filter('LeftLowArm', isEqual=True)[0]
print(f'\nLeftLowArm properties:')
print(f'Position:\t{arm.pointToWorld((0,0,0))}')
print(f'Y-Dir:\t\t{arm.UpWorld}')
print(f'X-Dir:\t\t{arm.RightWorld}')


# get position of joints within the space of the right leg.
# be aware of applied scaling here! Only the root joint has scaling in this example.
print(f'\nPositions in LeftUpLeg space:')
rightleg = bvh.Hierarchy.filter('LeftUpLeg')[0]
for joint, index, depth in rightleg.layout():
    worldPosition = joint.pointToWorld((0,0,0))
    localPosition = rightleg.pointToLocal(worldPosition)
    print(f'{localPosition} {joint.Name}')

# LeftLowArm properties:
# Position:	vec3(    -0.162209,      1.14091,      1.51718 )
# Y-Dir:		vec3(     0.912751,    -0.113158,      0.39253 )
# X-Dir:		vec3(    -0.349098,    -0.715101,     0.605609 )

# Positions in LeftUpLeg space:
# vec3(  2.86102e-06,  -3.8147e-06,   3.8147e-06 ) LeftUpLeg
# vec3(  4.52995e-06, -7.15256e-07,       -18.34 ) LeftLowLeg
# vec3(     -2.87719,     -13.3042,     -29.1305 ) LeftFoot
```
### Compare pose data
```python
# Loads the pose, then extracts from all joints their positions in world space
pose0positions = [joint.pointToWorld((0,0,0)) for (joint, index, depth) in bvh.Hierarchy.readPose(0).layout()]
pose1positions = [joint.pointToWorld((0,0,0)) for (joint, index, depth) in bvh.Hierarchy.readPose(1).layout()]

print('Change in position:')
for (joint, index, depth) in bvh.Hierarchy.layout():
    print(f'{pose1positions[index] - pose0positions[index]} {joint.Name}')

# Change in position:
# vec3(        -0.22,    0.0900002,        -1.89 ) Hips
# vec3(    -0.219298,    0.0907593,     -1.89325 ) Chest
# vec3(    -0.213268,     0.078064,     -1.91529 ) Neck
# vec3(    -0.212836,    0.0711365,     -1.91729 ) Head
# vec3(    -0.214325,     0.077774,     -1.91125 ) LeftCollar
# vec3(    -0.209374,    0.0882034,     -1.93187 ) LeftUpArm
# vec3(    -0.207287,     0.119064,     -1.91724 ) LeftLowArm
# vec3(    -0.212839,     0.131844,     -1.93034 ) LeftHand
# vec3(    -0.214348,    0.0771713,     -1.91111 ) RightCollar
# vec3(    -0.219791,    0.0777321,     -1.88764 ) RightUpArm
# vec3(    -0.218666,    0.0549126,      -1.8903 ) RightLowArm
# vec3(    -0.197209,    0.0386162,     -1.90305 ) RightHand
# vec3(    -0.220793,    0.0919762,     -1.89322 ) LeftUpLeg
# vec3(    -0.233757,    0.0889778,     -1.93163 ) LeftLowLeg
# vec3(    -0.203906,    0.0927582,      -1.9287 ) LeftFoot
# vec3(    -0.219207,    0.0880241,     -1.88678 ) RightUpLeg
# vec3(    -0.213404,    0.0810432,     -1.87141 ) RightLowLeg
# vec3(    -0.215267,    0.0892754,     -1.85474 ) RightFoot
```
