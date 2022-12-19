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
# this is this is the original motion data, rotation are converted to quaternions
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
# the root position has to be updated to the scale to if there is no root bone!
bvh.Hierarchy.Scale = (0.02, 0.02, 0.02)
bvh.Hierarchy.Position *= bvh.Hierarchy.Scale

# get world space position of all joints
for joint, index, depth in bvh.Hierarchy.layout():
    print(f'Position: {joint.pointToWorld((0,0,0))} {joint.Name}')

# read data for a single joint
arm = bvh.Hierarchy.select('LeftLowArm', isEqual=True)[0]
print(f'\nLeftLowArm:')
print(f'Position:\t{arm.pointToWorld((0,0,0))}')
print(f'Y-Dir:\t\t{arm.UpWorld}')
print(f'X-Dir:\t\t{arm.RightWorld}')

# Position: vec3(       0.1606,       0.7002,       1.7672 ) Hips
# Position: vec3(     0.166593,     0.800774,      1.79378 ) Chest
# Position: vec3(     0.183282,      1.13198,      1.62304 ) Neck
# Position: vec3(     0.201143,      1.16631,      1.52114 ) Head
# Position: vec3(     0.160555,      1.07221,      1.61062 ) LeftCollar
# Position: vec3(    0.0533372,      1.10009,      1.61253 ) LeftUpArm
# Position: vec3(    -0.162209,      1.14091,      1.51718 ) LeftLowArm
# Position: vec3(    -0.120072,      1.00391,      1.37971 ) LeftHand
# Position: vec3(     0.205259,      1.07142,      1.61344 ) RightCollar
# Position: vec3(     0.321048,      1.10524,      1.62711 ) RightUpArm
# Position: vec3(     0.555624,      1.13019,      1.61172 ) RightLowArm
# Position: vec3(     0.578145,      1.29305,      1.47631 ) RightHand
# Position: vec3(    0.0851123,     0.699307,       1.7876 ) LeftUpLeg
# Position: vec3(    0.0180001,     0.345904,      1.85933 ) LeftLowLeg
# Position: vec3(  -0.00783825,     0.189567,      2.16848 ) LeftFoot
# Position: vec3(     0.236088,     0.701093,       1.7468 ) RightUpLeg
# Position: vec3(     0.296095,     0.398319,      1.57635 ) RightLowLeg
# Position: vec3(     0.342655,    0.0917735,      1.72255 ) RightFoot

# LeftLowArm:
# Position:	vec3(    -0.162209,      1.14091,      1.51718 )
# Y-Dir:		vec3(     0.912752,    -0.113158,      0.39253 )
# X-Dir:		vec3(    -0.349097,      -0.7151,     0.605609 )
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
# vec3(     -0.18489,     0.127953,     -2.05244 ) Chest
# vec3(     0.116602,    -0.506794,     -3.15424 ) Neck
# vec3(     0.138187,    -0.853119,     -3.25434 ) Head
# vec3(    0.0637407,    -0.521355,     -2.95226 ) LeftCollar
# vec3(     0.311289,   0.00019455,     -3.98365 ) LeftUpArm
# vec3(     0.415657,      1.54335,       -3.252 ) LeftLowArm
# vec3(      0.13809,      2.18234,     -3.90731 ) LeftHand
# vec3(    0.0625801,    -0.551456,     -2.94576 ) RightCollar
# vec3(    -0.209536,    -0.523285,     -1.77232 ) RightUpArm
# vec3(    -0.153286,     -1.66424,     -1.90514 ) RightLowArm
# vec3(     0.919542,     -2.47902,     -2.54264 ) RightHand
# vec3(    -0.259668,     0.188808,     -2.05069 ) LeftUpLeg
# vec3(    -0.907879,    0.0389862,      -3.9713 ) LeftLowLeg
# vec3(     0.584709,      0.22802,     -3.82487 ) LeftFoot
# vec3(     -0.18033,  -0.00880814,     -1.72931 ) RightUpLeg
# vec3(      0.10982,    -0.357864,    -0.960358 ) RightLowLeg
# vec3(    0.0166397,    0.0537415,    -0.127296 ) RightFoot
```
