import glm
from SpatialTransform import Transform
from ..shared import Pose


class Joint(Transform):
    """Transform data of a joint including its keyframes.

    DataBVH holds the original bvh data of the hierarchy and motion.

    Keyframes holding the converted motion data, where position and rotation are in local space, in cluding the bvh base pose"""

    @property
    def Parent(self) -> "Joint": return self._Parent

    @property
    def Children(self) -> list["Joint"]: return self._Children

    @property
    def CurrentFrame(self) -> int: return self._CurrentFrame

    @property
    def Keyframes(self) -> list[Pose]: return self._Keyframes
    @Keyframes.setter
    def Keyframes(self, value: list[Pose]) -> None: self._Keyframes = list(value)

    def __init__(self, name: str, position: glm.vec3 = glm.vec3(), rotation: glm.quat = glm.quat(), scale: glm.vec3 = glm.vec3(1), emptyKeyframes: int = 0) -> None:
        super().__init__(name, position, rotation, scale)
        self._Parent: "Joint" = None
        self._Children: list["Joint"] = []

        if emptyKeyframes > 0:
            self._Keyframes: list[Pose] = [Pose(self._PositionLocal, self.RotationLocal, self.ScaleLocal) for _ in range(emptyKeyframes)]
            self.readPose(0)
        else:
            self._Keyframes: list[Pose] = []
            self._CurrentFrame = -1

    def readPose(self, frame: int, recursive: bool = True) -> "Joint":
        """Sets the transform position and rotation properties by the given keyframe.

        If recursive the children do also load their keyframe data."""
        if frame < 0: frame += len(self.Keyframes)
        if frame < 0 or frame >= len(self._Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self._Keyframes)} Keyframes)')

        self._CurrentFrame = frame
        self.PositionLocal = self._Keyframes[frame].Position
        self.RotationLocal = self._Keyframes[frame].Rotation
        self.ScaleLocal = self._Keyframes[frame].Scale

        if recursive:
            for child in self.Children:
                child.readPose(frame, recursive)
        return self

    def writePose(self, frame: int, recursive: bool = True) -> "Joint":
        """Sets the keyframe properties by the current transform local position and local rotation.

        If recursive the children do also update their keyframe data."""
        if frame < 0: frame += len(self.Keyframes)
        if frame < 0 or frame > len(self._Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range.')

        elif frame < len(self._Keyframes):
            self._Keyframes[frame].Position = self.PositionLocal
            self._Keyframes[frame].Rotation = self.RotationLocal
            self._Keyframes[frame].Scale = self.ScaleLocal

        elif frame == len(self._Keyframes):
            self._Keyframes.append(Pose(self.PositionLocal, self.RotationLocal))

        if recursive:
            for child in self.Children:
                child.writePose(frame)
        return self

    def attach(self, *nodes: "Joint", keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        for node in nodes:
            # attach the joint
            super().attach(node, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale)

            # apply attach corrections to animation data
            for pose in node._Keyframes:
                if keepPosition: pose.Position = self.SpaceWorldInverse * pose.Position
                if keepRotation: pose.Rotation = self.RotationWorldInverse * pose.Rotation
                if keepScale: pose.Scale = self.ScaleWorldInverse * pose.Scale
        return self

    def detach(self, node: "Joint", keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":

        # apply detach corrections to animation data
        for pose in node._Keyframes:
            if keepPosition: pose.Position = self.SpaceWorld * pose.Position
            if keepRotation: pose.Rotation = self.RotationWorld * pose.Rotation
            if keepScale: pose.Scale = self.ScaleWorld * pose.Scale

        # finally detatch the joint
        return super().detach(node, keepPosition, keepRotation, keepScale)

    def clearParent(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        return super().clearParent(keepPosition, keepRotation, keepScale)

    def clearChildren(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        return super().clearChildren(keepPosition, keepRotation, keepScale)

    def applyPosition(self, position: glm.vec3 = None, recursive: bool = False) -> "Joint":
        # define positional change
        change = -self.PositionLocal if position is None else position
        changeInverse = glm.inverse(self.RotationLocal) * (glm.div(1, self.ScaleLocal) * -change)

        # apply to current data
        super().applyPosition(position, recursive=recursive)

        # apply to keyframes
        for pose in self._Keyframes:
            pose.Position += change
        for child in self._Children:
            for pose in child._Keyframes:
                pose.Position += changeInverse

        return self

    def applyRotation(self, rotation: glm.quat = None, recursive: bool = False) -> "Joint":
        # define rotational change
        change = glm.inverse(self.RotationLocal) if rotation is None else rotation
        changeInverse = glm.inverse(change)

        # apply to current data
        super().applyRotation(rotation, recursive=False)

        # apply to keyframes
        for pose in self._Keyframes:
            pose.Rotation = change * pose.Rotation
        for child in self._Children:
            for pose in child._Keyframes:
                pose.Position = changeInverse * pose.Position
                pose.Rotation = changeInverse * pose.Rotation
            if recursive:
                child.applyRotation(rotation, recursive=True)

        return self

    def appyScale(self, scale: glm.vec3 = None, recursive: bool = False) -> "Joint":
        # define change in scale
        changeFrame = glm.div(self.ScaleLocal, self._Keyframes[self._CurrentFrame].Scale)
        change = glm.div(1, self.ScaleLocal) if scale is None else scale
        changeInverse = glm.div(1, change)

        # apply to current data
        super().appyScale(scale, recursive=False)

        # apply to keyframes
        for pose in self._Keyframes:
            pose.Scale *= changeFrame * change
        for child in self._Children:
            for pose in child._Keyframes:
                pose.Position *= changeInverse
                pose.Scale *= changeInverse
            if recursive:
                child.appyScale(scale, recursive=True)

        return self

    def roll(self, degrees: float, recursive: bool = False) -> "Joint":
        """Rolls the joint along its local Y axis. Updates the children so there is no spatial change

        Returns itself"""
        change = glm.angleAxis(glm.radians(degrees), (0, 1, 0))
        changeInverse = glm.inverse(change)

        self.RotationLocal = self.RotationLocal * change
        for pose in self._Keyframes:
            pose.Rotation = pose.Rotation * change

        for child in self._Children:
            child.PositionLocal = changeInverse * child.PositionLocal
            child.RotationLocal = changeInverse * child.RotationLocal
            for pose in child._Keyframes:
                pose.Position = changeInverse * pose.Position
                pose.Rotation = changeInverse * pose.Rotation
            if recursive: child.roll(degrees, recursive=True)

        return self

    def filter(self, pattern: str, isEqual: bool = False, caseSensitive: bool = False) -> list["Joint"]:
        return super().filter(pattern, isEqual, caseSensitive)

    def filterRegex(self, pattern: str) -> list["Joint"]:
        return super().filterRegex(pattern)

    def layout(self, index: int = 0, depth: int = 0) -> list[tuple["Joint", int, int]]:
        return super().layout(index, depth)
