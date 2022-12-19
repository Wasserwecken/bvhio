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
# Defines the base pose with the hierarchical joint data, including calculated bone orientation
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
bvh.Hierarchy.readPose(0) # first the pose has to be set

# get world space position of all joints
for joint, index, depth in bvh.Hierarchy.layout():
    print(f'Position: {joint.pointToWorld((0,0,0))} {joint.Name}')
print()

# read data for a single joint
arm = bvh.Hierarchy.select('LeftLowArm', isEqual=True)[0]
print(f'Position:\t{arm.pointToWorld((0,0,0))}')
print(f'Y-Dir:\t\t{arm.UpWorld}')
print(f'X-Dir:\t\t{arm.RightWorld}')
```
### Compare pose data
```python
# Loads the pose, then extracts from all joints their positions in world space
pose0positions = [joint.pointToWorld((0,0,0)) for (joint, index, depth) in bvh.Hierarchy.readPose(0).layout()]
pose1positions = [joint.pointToWorld((0,0,0)) for (joint, index, depth) in bvh.Hierarchy.readPose(1).layout()]

for (joint, index, depth) in bvh.Hierarchy.layout():
    print(f'Diff: {pose1positions[index] - pose0positions[index]} {joint.Name}')


# same code but different iteration approach
for (joint, index, depth) in bvh.Hierarchy.layout():
    pose0 = bvh.Hierarchy.readPose(0).pointToWorld((0,0,0))
    pose1 = bvh.Hierarchy.readPose(1).pointToWorld((0,0,0))
    print(f'Diff: {pose0 - pose1} {joint.Name}')
```
