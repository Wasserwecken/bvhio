import glm
import bisect
from SpatialTransform import Transform, Pose


class Joint(Transform):
    """Spatial definition of an linear space with position, rotation and scale.
    - Bone alignment is expected to be along the Y+ axis.
    - Space is defined as right handed where Y+:up and X+:right and Z-:forward.
    - Positive rotations are counter clockwise.
    - The animation is a cualculation of ``Pose = RestPose + Keyframe``
    - The RestPose and Keyframe data is in local space only.
    - The method ``readPose()`` combines the RestPose and Keframes."""

    @property
    def Parent(self) -> "Joint":
        return self._Parent

    @property
    def Children(self) -> list["Joint"]:
        return self._Children

    @property
    def CurrentFrame(self) -> int:
        """Latest frame index that has been read with readPose()."""
        return self._CurrentFrame

    @property
    def Keyframes(self) -> list[tuple[int, Transform]]:
        """Animation data for the joint. A keyframe holds the change of local properties in relation to the rest pose, so that ``Pose = RestPose + Keyframe``.
    - The first element in the tuple is the frame id and the second element are the local keyframe properties.
    - This is an ordered list by the frame id.
    - Negative frame ids should not exist."""
        return self._Keyframes

    @Keyframes.setter
    def Keyframes(self, value: list[tuple[int, Transform]]) -> None:
        self._Keyframes = list(value)
        self.RestPose.clearChildren(keep=[None])
        self.RestPose.attach(*[key for frame, key in value], keep=[None])

    @property
    def RestPose(self) -> Transform:
        """Pose without any keyframe applied. The common T-Pose would go here. This Pose is the base for all animation data."""
        return self._RestPose

    @RestPose.setter
    def RestPose(self, value: Pose) -> None:
        self._RestPose = value.duplicate()

    def __init__(
            self, name: str = None,
            position: glm.vec3 = None,
            rotation: glm.quat = None,
            scale: glm.vec3 = None,
            restPose: Transform = None,
            keyFrames: list[tuple[int, Transform]] = None) -> None:

        super().__init__(name, position, rotation, scale)
        self._Parent: "Joint" = None
        self._Children: list["Joint"] = []

        self._RestPose: Transform = Transform(name='RestPose') if restPose is None else restPose
        self._Keyframes: list[tuple[int, Transform]] = [] if keyFrames is None else keyFrames
        self._CurrentFrame = -1

    def getKeyframe(self, frame: int) -> Transform:
        """Returns the pose at the given frame id.
        - If the frame number is negative, it will look for the n-th frame from the end.
        - If there are no keyframes, the joint propetries will not change.
        - If the frame id is out of the keyframe length, the nearest keyframe propetires are used.
        - If the frame id is between two keyframes, pose properties are linearly interpolated."""
        if len(self.Keyframes) == 0:
            key = Transform(name=f'Key {frame} (placeholder)')
            self.RestPose.duplicate(recursive=False).attach(key, keep=None)
            return key

        if frame < 0: frame = max(0, self.getKeyframeRange(includeChildren=False)[1] + 1 - frame)

        # pose definition
        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)
        if index == len(self.Keyframes):
            # index is bigger than last frame, take last key
            return self.Keyframes[-1][1]
        elif self.Keyframes[index][0] == frame:
            # index matches a keyframe
            return self.Keyframes[index][1]
        else:
            if index == 0:
                # index is smaller than first frame, take first key
                return self.Keyframes[-1][1]
            else:
                # index is in between two keyframes, interpolate
                before = self.Keyframes[index - 1]
                after = self.Keyframes[index]
                weight = (before[0] + frame) / after[0]

                restPoseCopy = self.RestPose.duplicate(recursive=False).attach(
                    Transform(
                        name=f'Key {frame} (interpolated)',
                        position=glm.lerp(before[1].Position, after[1].Position, weight),
                        rotation=glm.lerp(before[1].Rotation, after[1].Rotation, weight),
                        scale=glm.lerp(before[1].Scale, after[1].Scale, weight)
                    ), keep=None
                )
                return restPoseCopy.Children[0]

    def setKeyframe(self, frame: int, pose: Transform, keep: list[str] = ['position', 'rotation', 'scale']) -> "Joint":
        """Inserts the given pose to the the keyframes.
        - If there is already a keyframe at the frame id, it will be overwritten.
        - If the frame number is negative, it counts as the n-th frame from the end.
        - This pose is added later to the rest pose to calculate the final animation."""
        if frame < 0: frame = max(0, self.getKeyframeRange(includeChildren=False)[1] + 1 - frame)
        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)

        if index == len(self.Keyframes) or self.Keyframes[index][0] != frame:
            newKey = Transform(name=f'Key {frame}', position=pose.Position, rotation=pose.Rotation, scale=pose.Scale)
            bisect.insort(self.Keyframes, (frame, newKey))
            self.RestPose.attach(newKey, keep=keep)
        else:
            if 'position' in keep: self.Keyframes[index][1].PositionWorld = pose.Position
            else: self.Keyframes[index][1].Position = pose.Position

            if 'rotation' in keep: self.Keyframes[index][1].RotationWorld = pose.Rotation
            else: self.Keyframes[index][1].Rotation = pose.Rotation

            if 'scale' in keep: self.Keyframes[index][1].ScaleWorld = pose.Scale
            else: self.Keyframes[index][1].Scale = pose.Scale

        return self

    def removeKeyframe(self, frame: int, recursive: bool = False) -> "Joint":
        """Removes the keyframe, if it exists, from the keyframe list.
        - If recursive is True -> Child joints do also load their rest pose.

        Returns itself."""
        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)

        if index != len(self.Keyframes) and self.Keyframes[index][0] == frame:
            self.Keyframes.pop(index)[1].clearParent(keep=None)

        if recursive:
            for child in self.Children:
                child.removeKeyframe(frame=frame, recursive=True)

        return self

    def loadKeyframe(self, frame: int, recursive: bool = True, use: bool = ['position', 'rotation', 'scale']) -> "Joint":
        """Loads the pose at the given frame into the transforms properties.
        - This is the animation data without rest pose.

        Returns itself."""
        key = self.getKeyframe(frame)

        if 'position' in use: self.Position = key.Position
        if 'rotation' in use: self.Rotation = key.Rotation
        if 'scale' in use: self.Scale = key.Scale

        if recursive:
            for child in self.Children:
                child.loadKeyframe(frame=frame, recursive=True, use=use)

        return self

    def loadRestPose(self, recursive: bool = True, use: bool = ['position', 'rotation', 'scale']) -> "Joint":
        """Sets joint properties to the rest pose.
        - If recursive is True -> Child joints do also load their rest pose.

        Returns itself."""
        # self alignment
        if 'position' in use: self.Position = self.RestPose.Position
        if 'rotation' in use: self.Rotation = self.RestPose.Rotation
        if 'scale' in use: self.Scale = self.RestPose.Scale

        # recursion
        if recursive:
            for child in self.Children:
                child.loadRestPose(recursive=True, use=use)

        return self

    def writeRestPose(self, recursive: bool = True, keep: list[str] = ['position', 'rotation', 'scale']) -> "Joint":
        """Sets the rest pose to the current joint properties.
        - If keep contains properties -> The Keyframes are modified to keep its spatial algiment in world space.
        - If keep is None or empty -> Keyframes do not change and thus the animation will change.
        - If recursive is True -> Child joints do also load their rest pose.

        Returns itself."""
        # remove change in rest pose from keyframes
        if keep:
            for frame, key in self.Keyframes:
                if 'position' in keep: key.Position = self.SpaceInverse * key.PositionWorld
                if 'rotation' in keep: key.Rotation = glm.inverse(self.Rotation) * key.RotationWorld
                if 'scale' in keep: key.Scale = (key.Scale / self.ScaleWorld)

        # write rest pose
        self.RestPose.Position = self.Position
        self.RestPose.Rotation = self.Rotation
        self.RestPose.Scale = self.Scale

        # recursion
        if recursive:
            for child in self.Children:
                child.writeRestPose(recursive=True, keep=keep)

        return self

    def loadPose(self, frame: int, recursive: bool = True, use: bool = ['position', 'rotation', 'scale']) -> "Joint":
        """Sets joint properties to the animation at the given frame id. The animation is defined as 'Pose = RestPose + Keyframe'.
        - If the frame number is negative, it will look for the n-th frame from the end.
        - If there are no keyframes, the joint propetries will not change.
        - If the frame id is out of the keyframe length, the nearest keyframe propetires are used.
        - If the frame id is between two keyframes, pose properties are linearly interpolated.
        - If recursive is True -> Child joints do also load their pose.

        Returns itself."""
        # get animation data
        key = self.getKeyframe(frame)

        # set animation pose, world space includes the transform from the rest pose
        self._CurrentFrame = frame
        if 'position' in use: self.Position = key.PositionWorld
        if 'rotation' in use: self.Rotation = key.RotationWorld
        if 'scale' in use: self.Scale = key.ScaleWorld

        # may do it recursively
        if recursive:
            for child in self.Children:
                child.loadPose(frame, recursive=True, use=use)

        return self

    def writePose(self, frameId: int, recursive: bool = True) -> "Joint":
        """Sets joint properties as animation pose for the given frame id.
        - If there is already a keyframe at the frame id, it will be overwritten.
        - Inserts a new keyframe if there is none yet.
        - If the frame number is negative, it counts as the n-th frame from the end.
        - If recursive is True -> Child joints do also write their pose.

        Returns itself."""
        # add keyframe
        self.setKeyframe(frameId, pose=self, keep=['position', 'rotation', 'scale'])

        # recursion
        if recursive:
            for child in self.Children:
                child.writePose(frameId, recursive=True)

        return self

    def getKeyframeRange(self, includeChildren: bool = True) -> tuple[int, int]:
        """Returns the earliest and latest frame id of the animation.
        - If there are no keyframes, `(0, 0)` is returned.
        - If includeChildren is True -> The range considers the earliest and latest frames from its children too.
        The tuple layout is -> [FirstFrameId, LastFrameId]"""
        if len(self.Keyframes) == 0: return (0, 0)
        range = (self.Keyframes[0][0], self.Keyframes[-1][0])

        if includeChildren:
            for child in self.Children:
                childRange = child.getKeyframeRange(includeChildren=True)
                range = (min(range[0], childRange[0]), max(range[1], childRange[1]))

        return range

    def roll(self, degrees: float, recursive: bool = False) -> "Joint":
        """Rotates the joint along its local Y axis and updates the children so there is no spatial change.
        - RestPose and Keyframe data are not modified.

        Returns itself.
        """
        change = glm.angleAxis(glm.radians(degrees), (0, 1, 0))
        changeInverse = glm.inverse(change)

        self.Rotation = self.Rotation * change
        for child in self.Children:
            child.Position = changeInverse * child.Position
            child.Rotation = changeInverse * child.Rotation

            if recursive:
                child.roll(degrees, recursive=True)

        return self

    def attach(self, *nodes: "Joint", keep: list[str] = ['position', 'rotation', 'scale']) -> "Joint":
        return super().attach(*nodes, keep=keep)

    def detach(self, *nodes: "Joint", keep: list[str] = ['position', 'rotation', 'scale']) -> "Joint":
        return super().detach(*nodes, keep=keep)

    def clearParent(self, keep: list[str] = ['position', 'rotation', 'scale']) -> "Joint":
        return super().clearParent(keep=keep)

    def clearChildren(self, keep: list[str] = ['position', 'rotation', 'scale']) -> "Joint":
        return super().clearChildren(keep=keep)

    def applyPosition(self, position: glm.vec3 = None, recursive: bool = False) -> "Joint":
        return super().applyPosition(position, recursive)

    def applyRestposePosition(self, position: glm.vec3 = None, recursive: bool = False) -> "Joint":
        """"Resets the position of the Restpose to (0,0,0) or adds the given position.
        - This will load the restpose and overwrites the current pose of the transform!
        - You may want to call `loadPose` after this one or store the current properties.
        - Updates its keyframes position ONLY. Rotation and scale will be unchanged.
        - Updates its children Restposes positions to be spatially unchanged.
        - This does not update the childrens keyframes.

        Returns itself.
        """
        change, changeInverse = self.RestPose._applyPositionGetChanges(position)
        self.RestPose.applyPosition(position, recursive=False)

        for child in self.Children:
            child.RestPose._applyPositionChangeInverse(changeInverse)

            if recursive:
                child.applyRestposePosition(position=position, recursive=True)

        return self

    def applyRotation(self, rotation: glm.quat = None, recursive: bool = False, bake: bool = False) -> "Joint":
        return super().applyRotation(rotation, recursive, bake)

    def applyRestposeRotation(self, rotation: glm.quat = None, recursive: bool = False, bake: bool = False, bakeKeyframes: bool = False) -> "Joint":
        """"Resets the rotation of the Restpose to (1,0,0,0) or adds the given rotation.
        - This does not update the childrens keyframes.
        - If bake is True -> The childrens Restposes will change in position ONLY.
        - If bakeKeyframes is True -> Updates its keyframes position ONLY.

        Returns itself.
        """
        change, changeInverse = self.RestPose._applyRotationGetChanges(rotation)
        self.RestPose.applyRotation(rotation, recursive=False, bake=bakeKeyframes)

        for child in self.Children:
            child.RestPose._applyRotationChangeInverse(changeInverse, bake=bake)

            if recursive:
                child.applyRestposeRotation(rotation=rotation, recursive=True, bake=bake, bakeKeyframes=bakeKeyframes)

        return self

    def applyScale(self, scale: glm.vec3 = None, recursive: bool = False, bake: bool = False) -> "Joint":
        return super().applyScale(scale, recursive, bake)

    def applyRestposeScale(self, scale: glm.vec3 = None, recursive: bool = False, bake: bool = False, bakeKeyframes: bool = False) -> "Joint":
        """"Resets the scale of the Restpose to (1,1,1) or adds the given scale.
        - This does not update the childrens keyframes.
        - If bake is True -> The childrens Restposes will change in position ONLY.
        - If bakeKeyframes is True -> Updates its keyframes position ONLY.

        Returns itself.
        """
        change, changeInverse = self.RestPose._applyScaleGetChanges(scale)
        self.RestPose.applyScale(scale, recursive=False, bake=bakeKeyframes)

        for child in self.Children:
            child.RestPose._applyScaleChangeInverse(changeInverse, bake=bake)

            if recursive:
                child.applyRestposeScale(scale=scale, recursive=True, bake=bake, bakeKeyframes=bakeKeyframes)

        return self

    def setEuler(self, degrees: glm.vec3, order: str = 'ZXY', extrinsic: bool = True) -> "Joint":
        return super().setEuler(degrees, order, extrinsic)

    def filter(self, pattern: str, isEqual: bool = False, caseSensitive: bool = False) -> list["Joint"]:
        return super().filter(pattern, isEqual, caseSensitive)

    def filterRegex(self, pattern: str) -> list["Joint"]:
        return super().filterRegex(pattern)

    def layout(self, index: int = 0, depth: int = 0) -> list[tuple["Joint", int, int]]:
        return super().layout(index, depth)
