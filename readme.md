[![PyPI version](https://badge.fury.io/py/bvhio.svg)](https://pypi.python.org/pypi/bvhio/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Publish Main](https://github.com/Wasserwecken/bvhio/actions/workflows/publish_main.yml/badge.svg?branch=main)](https://github.com/Wasserwecken/bvhio/actions)
[![Publish Preview](https://github.com/Wasserwecken/bvhio/actions/workflows/publish_preview.yml/badge.svg?branch=preview)](https://test.pypi.org/project/bvhio/)
[![PyPI download month](https://img.shields.io/pypi/dm/bvhio.svg)](https://pypi.python.org/pypi/bvhio/)
[![Generic badge](https://img.shields.io/badge/Ask_me-anything-turquoise.svg)](https://github.com/Wasserwecken/bvhio/issues)
# bvhio
Lightweight libary for reading, editing and creating [Biovision .bvh](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html) files. Deserializes files into a hierarchical spatial structure like transforms in Unity or Unreal.

Data for each joint is provided in local and world space and does support modifing the hierarchy itself without losing the keyframe data. The spatial structure does also allow for editing the motion or rest pose data. This libary supports also deserializing and serialising .bvh files into a simplified structure that represents the key data from the file.

## Install
``` batch
pip install bvhio
 ```

## Why and intention
This libary is a side product of my master thesis, in order to extract conveniently local and world data features from a humanoid skeleton hierarchy. I could not find any libary that could do that, without bloat or the features I required for extraction or modification.

## Notes
- Right now, this libary can only read .bvh files. But it will be able to write .bvh in the future
- The package [spatial-transform](https://github.com/Wasserwecken/spatial-transform) is used as base object for joints and provides the most properties and methods.
- The package [PyGLM](https://github.com/Zuzu-Typ/PyGLM) is used for matrix, quaternion and vector calculations.
- Same coordination space as [openGL and GLM](https://www.evl.uic.edu/ralph/508S98/coordinates.html) is used. Which is: Right-Handed, - Y+ is up, Z- is forward and positive rotations are counter clockwise.

## Features
- Read/Write/Edit
    - Read and write .bvh files as simplified structure (`BvhJoint`).
    - Read and write .bvh files as transform hierarchy (`Joint`).
    - Animation data can be modified with both methods.
    - The transform hierarchy allows for easy modifications of rest and motion data.
- Animation
    - Supports modifing keyframe, rest positon and final pose data.
    - Supports joint special modifications, like changing the joint-roll
    - Keyframes are stored in local space and as difference to the rest pose.
    - Keyframes support Position, Rotation and Scale.
- Python
    - Every method is documented in code with docstrings.
    - Every method has type hinting.
    - ([Fluent Interface](https://de.wikipedia.org/wiki/Fluent_Interface)) design.


## Examples
### Read bvh as transform hierarchy
```python
import bvhio

# Reads the file into a transform tree structure and converts all data to build proper local and world spaces.
# This structure allows for extensive read of properties and spaces and does also support modifications of the animation.
root = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
root.printTree()

# load rest pose and print data
root.loadRestPose(recursive=True)
print('\nRest pose position and Y-direction of each joint in world space ')
for joint, index, depth in root.layout():
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

# Rest pose position and Y-direction of each joint in world space 
# vec3(            0,            0,            0 ) vec3(            0,            1,            0 ) Hips
# vec3(            0,         5.21,            0 ) vec3(            0,     0.997333,    0.0729792 ) Chest
# vec3(            0,        23.86,  1.19209e-07 ) vec3(            0,            1,            0 ) Neck
# vec3(            0,        29.31,  1.19209e-07 ) vec3(            0,            1,            0 ) Head
# vec3(         1.12,        21.44,         1.87 ) vec3(            1,  5.96046e-08,            0 ) LeftCollar
# vec3(         6.66,        21.44,         1.87 ) vec3(            0,           -1,            0 ) LeftUpArm
# vec3(         6.66,         9.48,         1.87 ) vec3(            0,           -1,            0 ) LeftLowArm
# vec3(         6.66,    -0.450002,         1.87 ) vec3(            0,           -1,            0 ) LeftHand
# vec3(        -1.12,        21.44,         1.87 ) vec3(           -1,  5.96046e-08,            0 ) RightCollar
# vec3(        -7.19,        21.44,         1.87 ) vec3(            0,           -1,            0 ) RightUpArm
# vec3(        -7.19,         9.62,         1.87 ) vec3(            0,           -1,            0 ) RightLowArm
# vec3(        -7.19,        -1.03,         1.87 ) vec3(            0,           -1,            0 ) RightHand
# vec3(         3.91,            0,            0 ) vec3(            0,           -1,            0 ) LeftUpLeg
# vec3(         3.91,       -18.34,            0 ) vec3(            0,           -1,            0 ) LeftLowLeg
# vec3(         3.91,       -35.71,            0 ) vec3(            0,           -1,            0 ) LeftFoot
# vec3(        -3.91,            0,            0 ) vec3(            0,           -1,            0 ) RightUpLeg
# vec3(        -3.91,       -17.63,            0 ) vec3(            0,           -1,            0 ) RightLowLeg
# vec3(        -3.91,       -34.77,            0 ) vec3(            0,           -1,            0 ) RightFoot
```

### Read bvh as simple structure
```python
import bvhio

# Reads the file into a deserialized tree structure.
bvh = bvhio.readAsBvh('bvhio/tests/example.bvh')
print(f'Root: {bvh.Root}')
print(f'Frames: {bvh.FrameCount}')
print(f'Frame time: {bvh.FrameTime}')

# Properties of joints in the bvh tree structure.
bvh.Root.Name
bvh.Root.Offset
bvh.Root.Channels
bvh.Root.EndSite
bvh.Root.Keyframes
bvh.Root.Children

# Calculated properties that depend on the hierarchy.
bvh.Root.getRotation()
bvh.Root.getLength()
bvh.Root.getTip()

# --------------------------- OUTPUT ---------------------------
# Root: Hips
# Frames: 2
# Frame time: 0.033333
```

### bvhio joint properties and methods
```python
import bvhio

# The 'Joint' object allows for reading and modifing animations.
# Most of the functionality is based on the package 'spatial-transform'.
hierarchy = bvhio.readAsHierarchy('bvhio/tests/example.bvh')

# joints from the hierarchy can be selected by their name
joint = hierarchy.filter('Head')[0]

# Some methods and properties have been added to work with keyframe and joint data
joint.Keyframes         # list of local animation data
joint.readPose(0)        # sets the transform data to a specific keyframe
joint.writePose(0)       # writes the current transform data into a keyframe
joint.roll(0)            # changes the rotation of a bone around its own axis without affcting the children

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

# The package allows to make modifcation on the animation data very conviniently.
root = bvhio.readAsHierarchy('bvhio/tests/example.bvh')

# Add a root bone to the hierarchy and set itself as 'root'.
root = bvhio.Joint('Root').attach(root)

# Scale so the data represent roughly meters, assuming the data is in inches.
# Because the scale is on the root and the rest pose, it is applied to all world space data.
# Keep in mind that local keyframe and child rest pose data is still in inches!
root.RestPose.Scale = 0.0254

# Set all joints to the first keyframe.
# The animation pose is calculated by -> Pose = RestPose + Keyframe.
root.loadPose(0)

# print info
print('\nPosition, Y-direction and local scale of each joint in world space ')
for joint, index, depth in root.layout():
    print(f'{joint.PositionWorld} {joint.UpWorld} {joint.Scale} {joint.Name}')

# --------------------------- OUTPUT ---------------------------
# Position, Y-direction and local scale of each joint in world space 
# vec3(            0,            0,            0 ) vec3(            0,            1,            0 ) vec3(       0.0254,       0.0254,       0.0254 ) Root
# vec3(     0.203962,     0.889254,      2.24434 ) vec3(    0.0575125,     0.965201,     0.255108 ) vec3(            1,            1,            1 ) Hips
# vec3(     0.211573,      1.01698,       2.2781 ) vec3(    0.0481175,     0.852046,    -0.521251 ) vec3(            1,            1,            1 ) Chest
# vec3(     0.232768,      1.43762,      2.06126 ) vec3(     0.163858,     0.314978,    -0.934847 ) vec3(            1,            1,            1 ) Neck
# vec3(     0.255451,      1.48122,      1.93185 ) vec3(     0.136333,     0.863658,    -0.485292 ) vec3(            1,            1,            1 ) Head
# vec3(     0.203905,      1.36171,      2.04548 ) vec3(    -0.967669,     0.251636,    0.0172419 ) vec3(            1,            1,            1 ) LeftCollar
# vec3(    0.0677382,      1.39712,      2.04791 ) vec3(    -0.901112,     0.170623,    -0.398605 ) vec3(            1,            1,            1 ) LeftUpArm
# vec3(    -0.206005,      1.44895,      1.92682 ) vec3(     0.212169,    -0.689802,    -0.692213 ) vec3(            1,            1,            1 ) LeftLowArm
# vec3(    -0.152491,      1.27497,      1.75223 ) vec3(      0.21588,    -0.681081,    -0.699661 ) vec3(            1,            1,            1 ) LeftHand
# vec3(     0.260678,       1.3607,      2.04907 ) vec3(     0.953783,     0.278612,      0.11258 ) vec3(            1,            1,            1 ) RightCollar
# vec3(     0.407731,      1.40366,      2.06643 ) vec3(     0.992285,     0.105528,   -0.0650799 ) vec3(            1,            1,            1 ) RightUpArm
# vec3(     0.705642,      1.43534,      2.04689 ) vec3(     0.105734,     0.764633,    -0.635733 ) vec3(            1,            1,            1 ) RightLowArm
# vec3(     0.734244,      1.64218,      1.87492 ) vec3(     0.117056,     0.781042,    -0.613409 ) vec3(            1,            1,            1 ) RightHand
# vec3(     0.108093,      0.88812,      2.27025 ) vec3(    -0.182967,    -0.963474,     0.195551 ) vec3(            1,            1,            1 ) LeftUpLeg
# vec3(    0.0228602,     0.439299,      2.36134 ) vec3(   -0.0743765,    -0.450022,     0.889915 ) vec3(            1,            1,            1 ) LeftLowLeg
# vec3(  -0.00995459,      0.24075,      2.75397 ) vec3(   -0.0859881,    -0.463928,      0.88169 ) vec3(            1,            1,            1 ) LeftFoot
# vec3(     0.299831,     0.890388,      2.21844 ) vec3(     0.170185,    -0.858689,    -0.483414 ) vec3(            1,            1,            1 ) RightUpLeg
# vec3(      0.37604,     0.505865,      2.00197 ) vec3(     0.135822,     -0.89424,     0.426482 ) vec3(            1,            1,            1 ) RightLowLeg
# vec3(     0.435171,     0.116553,      2.18764 ) vec3(     0.188425,    -0.981787,    0.0242779 ) vec3(            1,            1,            1 ) RightFoot
```

### Compare pose data
```python
import bvhio

root = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
root = bvhio.Joint('Root', restPose=bvhio.Pose(scale=2.54)).attach(root)

# Load poses, then extract from all joints their position in world space.
pose0positions = [joint.PositionWorld for (joint, index, depth) in root.loadPose(0).layout()]
pose1positions = [joint.PositionWorld for (joint, index, depth) in root.loadPose(1).layout()]

print('Change in positions in centimeters between frame 0 and 1:')
for (joint, index, depth) in root.layout():
    print(f'{pose1positions[index] - pose0positions[index]} {joint.Name}')

# --------------------------- OUTPUT ---------------------------
# Change in positions in centimeters between frame 0 and 1:
# vec3(            0,            0,            0 ) Root
# vec3(    -0.558798,       0.2286,      -4.8006 ) Hips
# vec3(    -0.469618,     0.324989,     -5.21318 ) Chest
# vec3(     0.296169,     -1.28726,     -8.01178 ) Neck
# vec3(     0.350996,     -2.16693,     -8.26605 ) Head
# vec3(     0.161901,     -1.32426,     -7.49876 ) LeftCollar
# vec3(     0.790674,  0.000457764,     -10.1185 ) LeftUpArm
# vec3(      1.05577,      3.92007,     -8.26009 ) LeftLowArm
# vec3(     0.350739,      5.54311,     -9.92455 ) LeftHand
# vec3(     0.158957,     -1.40071,     -7.48221 ) RightCollar
# vec3(    -0.532215,     -1.32915,     -4.50168 ) RightUpArm
# vec3(    -0.389343,     -4.22717,     -4.83904 ) RightLowArm
# vec3(      2.33563,     -6.29668,     -6.45831 ) RightHand
# vec3(    -0.659554,     0.479576,     -5.20877 ) LeftUpLeg
# vec3(     -2.30601,    0.0990372,     -10.0871 ) LeftLowLeg
# vec3(      1.48517,     0.579193,     -9.71515 ) LeftFoot
# vec3(     -0.45804,    -0.022377,     -4.39243 ) RightUpLeg
# vec3(     0.278942,    -0.908985,     -2.43927 ) RightLowLeg
# vec3(     0.042263,      0.13649,    -0.323273 ) RightFoot
```

### Convert between bvh and hierarchy structure
```python
import bvhio


bvhRoot = bvhio.readAsBvh('bvhio/tests/example.bvh').Root
hierarchyRoot = bvhio.convertBvhToHierarchy(bvhRoot)
bvhRoot = bvhio.convertHierarchyToBvh(hierarchyRoot, hierarchyRoot.getKeyframeRange()[1])
```

### Interpolate between keyframes
```python
import bvhio

# load data
root = bvhio.readAsHierarchy('bvhio/tests/example.bvh')

# scales the frame id of the two given frames.
# this will restult in the ids 0 and 100.
# frames without keyframe are linearly interpolated.
for joint, index, depth in root.layout():
    joint.Keyframes = [(frame * 100, key) for frame, key in joint.Keyframes]

# persists the interpolations automatically
bvhio.writeHierarchy('test.bvh', root, 1/30)
```

### Create/build animations from code
```python
import bvhio

# create custom hierarchy.
root = bvhio.Joint('Root', (0,2,0)).setEuler((0,0,0)).attach(
    bvhio.Joint('UpperLegL', (+.3,2.1,0)).setEuler((0,0,180)).attach(
        bvhio.Joint('LowerLegL', (+.3,1,0)).setEuler((0,0,180))
    ),
    bvhio.Joint('UpperLegR', (-.3,2.1,0)).setEuler((0,0,180)).attach(
        bvhio.Joint('LowerLegR', (-.3,1,0)).setEuler((0,0,180))
    ),
)

# sets current layout as rest pose
root.writeRestPose(recursive=True)

# change the pose of the hierarchy to save it alter as key frame
# this will add a rotation to each leg joint for left and right side
for joint in root.filter('LegL'):
    joint.Rotation *= bvhio.Euler.toQuatFrom((+0.523599,0,0))
for joint in root.filter('LegR'):
    joint.Rotation *= bvhio.Euler.toQuatFrom((-0.523599,0,0))

# Persists the current pose as pose.
# This will calculate the keyframe differences to the rest pose.
root.writePose(0, recursive=True)

# The rest pose is loaded first to have the base pose again, this is not necessary.
root.loadRestPose(recursive=True)

# Now the same thing again with other rotations two have two keyframes.
for joint in root.filter('LegL'):
    joint.Rotation *= bvhio.Euler.toQuatFrom((-0.523599,0,0))
for joint in root.filter('LegR'):
    joint.Rotation *= bvhio.Euler.toQuatFrom((+0.523599,0,0))

# persists the current pose again as new pose.
# All keyframes between the first and this pose are linearly interpolated.
root.writePose(20, recursive=True)

# store the animation
bvhio.writeHierarchy('test.bvh', root, 1/30)


# --------------------------- OUTPUT (.bvh file) ---------------------------
# HIERARCHY
# ROOT Root
# {
#   OFFSET 0.0 2.0 0.0
#   CHANNELS 0 
#   JOINT UpperLegL
#   {
#     OFFSET 0.300000012 0.099999905 0.0
#     CHANNELS 3 Zrotation Xrotation Yrotation
#     JOINT LowerLegL
#     {
#       OFFSET 7e-09 -1.099999905 0.0
#       CHANNELS 3 Zrotation Xrotation Yrotation
#       End Site
#       {
#         OFFSET 8.7e-08 -1.0 0.0
#       }
#     }
#   }
#   JOINT UpperLegR
#   {
#     OFFSET -0.300000012 0.099999905 0.0
#     CHANNELS 3 Zrotation Xrotation Yrotation
#     JOINT LowerLegR
#     {
#       OFFSET 7e-09 -1.099999905 0.0
#       CHANNELS 3 Zrotation Xrotation Yrotation
#       End Site
#       {
#         OFFSET 8.7e-08 -1.0 0.0
#       }
#     }
#   }
# }
# MOTION
# Frames: 21
# Frame Time: 0.03333333333333333
# -7.75e-07 -30.000015259 -2.892e-06 -7.75e-07 -30.000015259 -2.892e-06 -7.75e-07 30.000015259 2.892e-06 -7.75e-07 30.000015259 2.892e-06 
# -6.1e-07 -26.743696213 -2.528e-06 -6.1e-07 -26.743696213 -2.528e-06 -6.1e-07 26.743696213 2.528e-06 -6.1e-07 26.743696213 2.528e-06 
# -4.7e-07 -23.57818985 -2.191e-06 -4.7e-07 -23.57818985 -2.191e-06 -4.7e-07 23.57818985 2.191e-06 -4.7e-07 23.57818985 2.191e-06 
# -3.52e-07 -20.487323761 -1.876e-06 -3.52e-07 -20.487323761 -1.876e-06 -3.52e-07 20.487323761 1.876e-06 -3.52e-07 20.487323761 1.876e-06 
# -2.54e-07 -17.457611084 -1.579e-06 -2.54e-07 -17.457611084 -1.579e-06 -2.54e-07 17.457611084 1.579e-06 -2.54e-07 17.457611084 1.579e-06 
# -1.74e-07 -14.477519989 -1.296e-06 -1.74e-07 -14.477519989 -1.296e-06 -1.74e-07 14.477519989 1.296e-06 -1.74e-07 14.477519989 1.296e-06 
# -1.1e-07 -11.536964417 -1.024e-06 -1.1e-07 -11.536964417 -1.024e-06 -1.1e-07 11.536964417 1.024e-06 -1.1e-07 11.536964417 1.024e-06 
# -6.1e-08 -8.626930237 -7.61e-07 -6.1e-08 -8.626930237 -7.61e-07 -6.1e-08 8.626930237 7.61e-07 -6.1e-08 8.626930237 7.61e-07 
# -2.7e-08 -5.739173412 -5.04e-07 -2.7e-08 -5.739173412 -5.04e-07 -2.7e-08 5.739173412 5.04e-07 -2.7e-08 5.739173412 5.04e-07 
# -7e-09 -2.865985394 -2.51e-07 -7e-09 -2.865985394 -2.51e-07 -7e-09 2.865985394 2.51e-07 -7e-09 2.865985394 2.51e-07 
# -0.0 0.0 -0.0 -0.0 0.0 -0.0 -0.0 0.0 -0.0 -0.0 0.0 -0.0 
# -7e-09 2.865985394 2.51e-07 -7e-09 2.865985394 2.51e-07 -7e-09 -2.865985394 -2.51e-07 -7e-09 -2.865985394 -2.51e-07 
# -2.7e-08 5.739173889 5.04e-07 -2.7e-08 5.739173889 5.04e-07 -2.7e-08 -5.739173889 -5.04e-07 -2.7e-08 -5.739173889 -5.04e-07 
# -6.1e-08 8.626929283 7.61e-07 -6.1e-08 8.626929283 7.61e-07 -6.1e-08 -8.626929283 -7.61e-07 -6.1e-08 -8.626929283 -7.61e-07 
# -1.1e-07 11.536964417 1.024e-06 -1.1e-07 11.536964417 1.024e-06 -1.1e-07 -11.536964417 -1.024e-06 -1.1e-07 -11.536964417 -1.024e-06 
# -1.74e-07 14.477519989 1.296e-06 -1.74e-07 14.477519989 1.296e-06 -1.74e-07 -14.477519989 -1.296e-06 -1.74e-07 -14.477519989 -1.296e-06 
# -2.54e-07 17.457611084 1.579e-06 -2.54e-07 17.457611084 1.579e-06 -2.54e-07 -17.457611084 -1.579e-06 -2.54e-07 -17.457611084 -1.579e-06 
# -3.52e-07 20.487323761 1.876e-06 -3.52e-07 20.487323761 1.876e-06 -3.52e-07 -20.487323761 -1.876e-06 -3.52e-07 -20.487323761 -1.876e-06 
# -4.7e-07 23.57818985 2.191e-06 -4.7e-07 23.57818985 2.191e-06 -4.7e-07 -23.57818985 -2.191e-06 -4.7e-07 -23.57818985 -2.191e-06 
# -6.1e-07 26.743696213 2.528e-06 -6.1e-07 26.743696213 2.528e-06 -6.1e-07 -26.743696213 -2.528e-06 -6.1e-07 -26.743696213 -2.528e-06 
# -7.75e-07 30.000015259 2.892e-06 -7.75e-07 30.000015259 2.892e-06 -7.75e-07 -30.000015259 -2.892e-06 -7.75e-07 -30.000015259 -2.892e-06 
```