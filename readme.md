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

## Examples and code
### Read bvh structure
```python
import bvhio

# reads the file into a deserialized structure.
# this structure does not have any specials properties or methods for spatial calculations
bvh = bvhio.readAsBVH('example.bvh')
print(f'Root: {bvh.Root}')
print(f'Frames: {bvh.FrameCount}')
print(f'Frame time: {bvh.FrameTime}')

# properties of a joint in the bvh hierarchy
bvh.Root.Name
bvh.Root.Offset
bvh.Root.Channels
bvh.Root.EndSite
bvh.Root.Keyframes
bvh.Root.Children

# calculated properties that depend on the hierarchy and file definition
bvh.Root.getRotation()
bvh.Root.getLength()
bvh.Root.getTip()

# --------------------------- OUTPUT ---------------------------
# Root: Hips
# Frames: 2
# Frame time: 0.033333
```

### Read bvh as transform hierarchy
```python
import bvhio

# reads the file into a deserialized structure. And provides all the bvh data as hierarchical transforms
# this structure allows for extensive read of properties and spaces and also supports modifications, inlcuding the keyframes
hierarchy = bvhio.read('example.bvh')
hierarchy.printTree()

# print info
print('\nPosition and Y-direction of each joint in world space')
for joint, index, depth in hierarchy.layout():
    print(f'{joint.PositionWorld} {joint.UpWorld} {joint.Name}')

# --------------------------- OUTPUT ---------------------------
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

# Position and Y-direction of each joint in world space
# vec3(            0,            0,            0 ) vec3(            0,            1,            0 ) Hips
# vec3(            0,       0.2605,            0 ) vec3(            0,     0.999986,   0.00532605 ) Chest
# vec3(            0,      1.19299,   0.00496654 ) vec3(            0,     0.999986,   0.00532605 ) Neck
# vec3(            0,      1.46548,   0.00641789 ) vec3(            0,     0.999986,   0.00532605 ) Head
# vec3(        0.056,      1.07149,    0.0978208 ) vec3(     0.998674,   0.00132638,  6.98492e-10 ) LeftCollar
# vec3(    0.0560001,     0.794495,    0.0963455 ) vec3(    -0.998674,    0.0013262, -6.98492e-10 ) LeftUpArm
# vec3(        0.654,     0.794495,    0.0963455 ) vec3(     0.998674,   0.00132638,  6.98492e-10 ) LeftLowArm
# vec3(       0.1575,     0.794495,    0.0963455 ) vec3(    -0.998674,    0.0013262, -6.98492e-10 ) LeftHand
# vec3(       -0.056,      1.07149,    0.0978208 ) vec3(    -0.998674,    0.0013262,            0 ) RightCollar
# vec3(       -0.056,     0.767995,    0.0962043 ) vec3(     0.998674,    0.0013262,            0 ) RightUpArm
# vec3(       -0.647,     0.767995,    0.0962043 ) vec3(    -0.998674,    0.0013262,            0 ) RightLowArm
# vec3(      -0.1145,     0.767995,    0.0962043 ) vec3(     0.998674,    0.0013262,            0 ) RightHand
# vec3(       0.1955,            0,            0 ) vec3(            0,           -1,            0 ) LeftUpLeg
# vec3(       0.1955,        0.917,            0 ) vec3(            0,            1,            0 ) LeftLowLeg
# vec3(       0.1955,    0.0484999,            0 ) vec3(            0,           -1,            0 ) LeftFoot
# vec3(      -0.1955,            0,            0 ) vec3(            0,           -1,            0 ) RightUpLeg
# vec3(      -0.1955,       0.8815,            0 ) vec3(            0,            1,            0 ) RightLowLeg
# vec3(      -0.1955,       0.0245,            0 ) vec3(            0,           -1,            0 ) RightFoot
```

### bvhio joint properties and methods
```python
import bvhio

# The 'Joint' object allows for reading and modifing animations.
# Most of the functionality is based on the package 'spatial-transform'.
hierarchy = bvhio.read('example.bvh')

# joints from the hierarchy can be selected by their name
joint = hierarchy.filter('Head')[0]

# Some methods and properties have been added to work with keyframe and joint data
joint.Keyframes         # list of local animation data
joint.readPose(0)        # sets the transform data to a specific keyframe
joint.writePose(0)       # writes the current transform data into a keyframe
joint.roll(0)            # changes the rotation of a bone around its own axis without affcting the children-

# Some methods do also update the keyframes to no destroy the animation data
# Please refer to the package 'spatial-transform' for their behaviour
joint.clearParent()
joint.clearChildren()
joint.attach()
joint.detach()
joint.applyPosition()
joint.applyRotation()
joint.appyScale()
```

### Interacting with joints and animation
```python
import bvhio

# The package allows to make modifcation on the animation data very conviniently
hierarchy = bvhio.read('example.bvh')

# add a root bone to the hierarchy
rootBone = bvhio.Joint('Root', (0,0,0), keyframePlaceholders=len(hierarchy.Keyframes))
rootBone.attach(hierarchy, keepPosition=True, keepRotation=True, keepScale=True)
hierarchy = rootBone

# keyframes can be easily modified, keep in mind that the keyframe data is local only
for pose in hierarchy.Keyframes: pose.Scale *= 10

# set and apply the scale so the positions represent roughly meters
# the 'appyScale' method recalculates local positions so the scale is included in the positions
# the 'appyScale' method does also update all keyframes data, so the scale will not be lost when another pose is read
hierarchy.ScaleWorld = 0.02
hierarchy.appyScale(recursive=True)

# rotate the whole animation because we can
hierarchy.setEuler((0, 180, 0))
hierarchy.applyRotation()

# sets all transforms to the last keyframe
# the local properties position, rotation and scale will be overwritten by the keyframe data
hierarchy.readPose(-1)

# print info
print('\nPosition and Y-direction of each joint in world space ')
for joint, index, depth in hierarchy.layout():
    print(f'{joint.PositionWorld} {joint.UpWorld} {joint.Name}')

# --------------------------- OUTPUT ---------------------------
# Position and Y-direction of each joint in world space
# vec3(            0,            0,            0 ) vec3(            0,            1,            0 ) Root
# vec3(       0.1562,        0.702,       1.7294 ) vec3(    0.0642514,     0.972485,     0.223931 ) Hips
# vec3(     0.162895,     0.803333,      1.75273 ) vec3(     0.061042,     0.851334,    -0.520683 ) Chest
# vec3(     0.185616,       1.1219,      1.56033 ) vec3(     0.167818,     0.251432,    -0.953215 ) Neck
# vec3(     0.203899,      1.14931,      1.45643 ) vec3(     0.140305,     0.829054,     -0.54128 ) Head
# vec3(      0.16182,      1.06187,       1.5519 ) vec3(    -0.922984,     0.345778,     -0.16893 ) LeftCollar
# vec3(    0.0594142,      1.10011,      1.53331 ) vec3(    -0.892385,      0.29965,     -0.33743 ) LeftUpArm
# vec3(    -0.154367,      1.17167,      1.45286 ) vec3(     0.184217,    -0.625452,    -0.758205 ) LeftLowArm
# vec3(    -0.117785,      1.04768,      1.30221 ) vec3(     0.182858,    -0.614945,    -0.767076 ) LeftHand
# vec3(     0.206499,      1.06048,      1.55484 ) vec3(     0.908953,     0.283253,     0.305897 ) RightCollar
# vec3(     0.316994,      1.09473,      1.59208 ) vec3(     0.997043,   0.00899994,   -0.0763166 ) RightUpArm
# vec3(     0.552958,      1.09674,      1.57422 ) vec3(     0.206468,     0.688129,    -0.695593 ) RightLowArm
# vec3(     0.597232,      1.24359,      1.42617 ) vec3(     0.224284,     0.704539,    -0.673291 ) RightHand
# vec3(    0.0799189,     0.703083,      1.74658 ) vec3(    -0.218311,    -0.971643,    0.0908292 ) LeftUpLeg
# vec3( -0.000157431,     0.346684,       1.7799 ) vec3(    0.0115528,    -0.439139,     0.898345 ) LeftLowLeg
# vec3(   0.00385598,     0.194127,      2.09198 ) vec3(    0.0255445,    -0.416461,     0.908795 ) LeftFoot
# vec3(     0.232481,     0.700917,      1.71222 ) vec3(     0.186643,    -0.878489,    -0.439798 ) RightUpLeg
# vec3(     0.298291,     0.391162,      1.55714 ) vec3(     0.130385,    -0.870226,     0.475086 ) RightLowLeg
# vec3(     0.342987,    0.0928484,         1.72 ) vec3(     0.186913,    -0.981388,    0.0440528 ) RightFoot
```

### Read joints
```python
# read data for a single joint
arm = hierarchy.filter('LeftLowArm', isEqual=True)[0]
print(f'\nLeftLowArm properties:')
print(f'Position: {arm.pointToWorld((0,0,0))}')
print(f'Y-Dir:    {arm.UpWorld}')
print(f'X-Dir:    {arm.RightWorld}')

# get position of joints within the space of the right leg.
# be aware of applied scaling here! Only the root joint has scaling in this example.
print(f'\nPositions in LeftUpLeg space:')
rightleg = hierarchy.filter('LeftUpLeg')[0]
for joint, index, depth in rightleg.layout():
    worldPosition = joint.pointToWorld((0,0,0))
    localPosition = rightleg.pointToLocal(worldPosition)
    print(f'{localPosition} {joint.Name}')

# LeftLowArm properties:
# Position: vec3(    -0.162209,      1.14091,      1.51718 )
# Y-Dir:    vec3(     0.912751,    -0.113158,      0.39253 )
# X-Dir:    vec3(    -0.349098,    -0.715101,     0.605609 )

# Positions in LeftUpLeg space:
# vec3(  2.86102e-06,  -3.8147e-06,   3.8147e-06 ) LeftUpLeg
# vec3(  4.52995e-06, -7.15256e-07,       -18.34 ) LeftLowLeg
# vec3(     -2.87719,     -13.3042,     -29.1305 ) LeftFoot
```
### Compare pose data
```python
import bvhio

# Loads the pose, then extracts from all joints their positions in world space
hierarchy = bvhio.read('example.bvh')
pose0positions = [joint.PositionWorld for (joint, index, depth) in hierarchy.readPose(0).layout()]
pose1positions = [joint.PositionWorld for (joint, index, depth) in hierarchy.readPose(1).layout()]

print('Change in position:')
for (joint, index, depth) in hierarchy.layout():
    print(f'{pose1positions[index] - pose0positions[index]} {joint.Name}')

# --------------------------- OUTPUT ---------------------------
# vec3(        -0.22,    0.0900002,        -1.89 ) Hips
# vec3(    -0.184891,     0.127953,     -2.05244 ) Chest
# vec3(     0.116364,    -0.505764,     -3.15356 ) Neck
# vec3(     0.138083,    -0.851955,     -3.25343 ) Head
# vec3(    0.0636444,    -0.520363,     -2.95185 ) LeftCollar
# vec3(     0.311055,   0.00294113,     -3.98363 ) LeftUpArm
# vec3(     0.417139,      1.54507,     -3.25227 ) LeftLowArm
# vec3(     0.137499,      2.18532,     -3.90658 ) LeftHand
# vec3(    0.0625172,    -0.550503,     -2.94523 ) RightCollar
# vec3(    -0.209719,    -0.523335,     -1.76971 ) RightUpArm
# vec3(     -0.15313,     -1.66174,     -1.89973 ) RightLowArm
# vec3(     0.920954,     -2.47511,     -2.53802 ) RightHand
# vec3(    -0.259668,     0.188808,     -2.05069 ) LeftUpLeg
# vec3(    -0.907878,      0.03899,     -3.97129 ) LeftLowLeg
# vec3(     0.584712,     0.228029,     -3.82486 ) LeftFoot
# vec3(    -0.180331,  -0.00880814,     -1.72931 ) RightUpLeg
# vec3(     0.109819,    -0.357868,     -0.96035 ) RightLowLeg
# vec3(    0.0166378,    0.0537376,    -0.127289 ) RightFoot
```
