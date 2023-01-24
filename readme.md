[![PyPI version](https://badge.fury.io/py/bvhio.svg)](https://badge.fury.io/py/bvhio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Publish Main](https://github.com/Wasserwecken/bvhio/actions/workflows/publish_main.yml/badge.svg?branch=main)
![Publish Preview](https://github.com/Wasserwecken/bvhio/actions/workflows/publish_preview.yml/badge.svg?branch=preview)
# bvhio
Lightweight libary for reading [Biovision .bvh](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html) files and converting them into a hierarchical spatial structure like transforms in Unity or Unreal.

Provide data for each joint in local and world space and does supports modifing the hierarchy itself without losing the keyframe data. The package [spatial-transform] is used as base object for joints and provides the most properties and methods.

## Install
``` batch
pip install bvhio
 ```

## Why and intention
This libary is a side product of my master thesis, in order to extract conveniently local and world data features from a humanoid skeleton hierarchy. I could not find any libary that could do that, without bloat or the features I required for extraction or modification.

## Notes
- Right now, this libary can only read .bvh files. But it will be able to write .bvh in the future
- The package [PyGLM](https://github.com/Zuzu-Typ/PyGLM) is used for matrix, quaternion and vector calculations.
- Same coordination space as [openGL and GLM](https://www.evl.uic.edu/ralph/508S98/coordinates.html) is used. Which is: Right-Handed, - Y+ is up, Z- is forward and positive rotations are counter clockwise.

## Features
- Deserialisation
    - load .bvh either as simple bvh structure or
    - load .bvh as transform hierarchy for full reading and modification capabilities
- Animation
    - Supports modifing keyframe data, even recursivly
    - Supports joint modifications, like changing the joint-roll
    - Keyframes are stored in local space
    - Keframes support Position, Rotation and Scale
- Python
    - Every method is documented in code with docstrings
    - Every method has type hinting
    - ([Fluent Interface](https://de.wikipedia.org/wiki/Fluent_Interface)) design


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

# add a root bone to the hierarchy and set itself as 'hierarchy'
hierarchy = bvhio.Joint('Root', (0,0,0), emptyKeyframes=len(hierarchy.Keyframes))\
    .attach(hierarchy, keepPosition=True, keepRotation=True, keepScale=True)

# keyframes can be easily modified, keep in mind that the keyframe data is in local space only
for pose in hierarchy.Keyframes:
    pose.Scale *= 10

# set and apply the scale so the positions represent roughly centimeters
# the 'appyScale' method recalculates local positions so the scale is included in the positions
# the 'appyScale' method does also update all keyframes data, so the scale will not be lost when another pose is read
hierarchy.ScaleWorld = 2.3
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
# vec3(       17.963,        80.73,      198.881 ) vec3(    0.0642514,     0.972485,     0.223931 ) Hips
# vec3(      18.7329,      92.3833,      201.564 ) vec3(     0.061042,     0.851334,    -0.520683 ) Chest
# vec3(      21.3459,      129.019,      179.438 ) vec3(     0.167818,     0.251432,    -0.953215 ) Neck
# vec3(      23.4484,      132.171,      167.489 ) vec3(     0.140305,     0.829054,     -0.54128 ) Head
# vec3(      18.6093,      122.116,      178.468 ) vec3(    -0.922984,     0.345778,     -0.16893 ) LeftCollar
# vec3(      6.83263,      126.512,       176.33 ) vec3(    -0.892385,      0.29965,     -0.33743 ) LeftUpArm
# vec3(     -17.7522,      134.742,      167.079 ) vec3(     0.184217,    -0.625452,    -0.758205 ) LeftLowArm
# vec3(     -13.5453,      120.483,      149.754 ) vec3(     0.182858,    -0.614945,    -0.767076 ) LeftHand
# vec3(      23.7474,      121.955,      178.806 ) vec3(     0.908953,     0.283253,     0.305897 ) RightCollar
# vec3(      36.4544,      125.894,       183.09 ) vec3(     0.997043,   0.00899994,   -0.0763166 ) RightUpArm
# vec3(      63.5902,      126.125,      181.035 ) vec3(     0.206468,     0.688129,    -0.695593 ) RightLowArm
# vec3(      68.6817,      143.013,      164.009 ) vec3(     0.224284,     0.704539,    -0.673291 ) RightHand
# vec3(      9.19068,      80.8546,      200.857 ) vec3(    -0.218311,    -0.971643,    0.0908292 ) LeftUpLeg
# vec3(   -0.0181017,      39.8687,      204.688 ) vec3(    0.0115528,    -0.439139,     0.898345 ) LeftLowLeg
# vec3(     0.443441,      22.3247,      240.578 ) vec3(    0.0255445,    -0.416461,     0.908795 ) LeftFoot
# vec3(      26.7353,      80.6054,      196.905 ) vec3(     0.186643,    -0.878489,    -0.439798 ) RightUpLeg
# vec3(      34.3035,      44.9836,      179.072 ) vec3(     0.130385,    -0.870226,     0.475086 ) RightLowLeg
# vec3(      39.4436,      10.6776,        197.8 ) vec3(     0.186913,    -0.981388,    0.0440528 ) RightFoot
```

### Compare pose data
```python
import bvhio

hierarchy = bvhio.read('example.bvh')

# Fluent API design allows you to do multiple actions in one line:
# Add root, scale down, apply scale, select first child, remove the parent
# This line is to scale the whole animation down and convert the scale into all local positions
hierarchy = bvhio.Joint('root', scale=2.3, emptyKeyframes=len(hierarchy.Keyframes))\
    .attach(hierarchy).appyScale(recursive=True).Children[0].clearParent()

# Loads the pose, then extracts from all joints their positions in world space
pose0positions = [joint.PositionWorld for (joint, index, depth) in hierarchy.readPose(0).layout()]
pose1positions = [joint.PositionWorld for (joint, index, depth) in hierarchy.readPose(1).layout()]

print('Change in positions in centimeters between frame 0 and 1:')
for (joint, index, depth) in hierarchy.layout():
    print(f'{pose1positions[index] - pose0positions[index]} {joint.Name}')

# --------------------------- OUTPUT ---------------------------
# Change in positions in centiometers between frame 0 and 1:
# vec3(    -0.506001,     0.207001,       -4.347 ) Hips
# vec3(    -0.425249,     0.294296,      -4.7206 ) Chest
# vec3(     0.267633,     -1.16325,     -7.25319 ) Neck
# vec3(     0.317589,     -1.95949,     -7.48289 ) Head
# vec3(     0.146381,     -1.19683,     -6.78926 ) LeftCollar
# vec3(     0.715426,    0.0067749,     -9.16235 ) LeftUpArm
# vec3(     0.959417,      3.55367,     -7.48021 ) LeftLowArm
# vec3(     0.316247,      5.02625,     -8.98512 ) LeftHand
# vec3(     0.143787,     -1.26615,       -6.774 ) RightCollar
# vec3(    -0.482353,     -1.20365,      -4.0703 ) RightUpArm
# vec3(    -0.352196,     -3.82198,     -4.36935 ) RightLowArm
# vec3(      2.11819,     -5.69276,      -5.8374 ) RightHand
# vec3(    -0.597237,     0.434265,      -4.7166 ) LeftUpLeg
# vec3(     -2.08812,    0.0896835,     -9.13399 ) LeftLowLeg
# vec3(      1.34484,     0.524475,     -8.79721 ) LeftFoot
# vec3(    -0.414764,   -0.0202637,      -3.9774 ) RightUpLeg
# vec3(     0.252583,    -0.823101,      -2.2088 ) RightLowLeg
# vec3(    0.0382652,     0.123592,     -0.29274 ) RightFoot
```
