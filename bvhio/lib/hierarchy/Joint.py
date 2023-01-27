import glm
import bisect
from SpatialTransform import Transform
from ..shared import Pose


class Joint(Transform):
    """Transform data of a joint including its keyframes.

    DataBVH holds the original bvh data of the hierarchy and motion.

    Keyframes holding the converted motion data, where position and rotation are in local space, in cluding the bvh base pose"""

    @property
    def Parent(self) -> "Joint":
        return self._Parent

    @property
    def Children(self) -> list["Joint"]:
        return self._Children

    @property
    def CurrentFrame(self) -> int:
        """Frame index that has been read the latest."""
        return self._CurrentFrame

    @property
    def Keyframes(self) -> list[tuple[int, Pose]]:
        """Poses for the joint. A pose holds the change of local properties in relation to the rest pose.

        The first element in the tuple is the frame id and the second element are the local pose properties."""
        return self._Keyframes

    @Keyframes.setter
    def Keyframes(self, value: list[tuple[int, Pose]]) -> None:
        self._Keyframes = list(value)

    @property
    def KeyframeRange(self) -> tuple[int, int]:
        frames = [key[0] for key in self.Keyframes]
        return [frames[0], frames[-1]]

    @property
    def RestPose(self) -> Pose:
        """Pose without any keyframe applied. The common T-Pose would go here."""
        return self._RestPose

    @RestPose.setter
    def RestPose(self, value: Pose) -> None:
        self._RestPose = value.copy()

    def __init__(
            self, name: str = None,
            position: glm.vec3 = None,
            rotation: glm.quat = None,
            scale: glm.vec3 = None,
            restPose: Pose = None,
            keyFrames: list[tuple[int, Pose]] = None) -> None:

        super().__init__(name, position, rotation, scale)
        self._Parent: "Joint" = None
        self._Children: list["Joint"] = []

        self._RestPose: Pose = Pose() if restPose is None else restPose
        self._Keyframes: list[tuple[int, Pose]] = [] if keyFrames is None else keyFrames
        self._CurrentFrame = -1

    def readRestPose(self, recursive: bool = True) -> "Joint":
        """Sets the joint to its rest pose.

        Returns itself."""
        # self alignment
        self.PositionLocal = self.RestPose.Position
        self.RotationLocal = self.RestPose.Rotation
        self.ScaleLocal = self.RestPose.Scale

        # recursion
        if recursive:
            for child in self.Children:
                child.readRestPose(recursive=True)
        return self

    def writeRestPose(self, recursive: bool = True, updateKeyframes: bool = True) -> "Joint":
        """Sets the rest pose to the current joint data.

        If updateKeyframes is NOT set, the keyframes will be untouched.

        If updateKeyframes IS set, the keyframes are updated to be spatially unchanged.

        Returns itself."""
        # animation data
        if updateKeyframes:
            for frame, pose in self.Keyframes:
                pose.Position += self.RestPose.Position - self.PositionLocal
                pose.Rotation *= self.RestPose.Rotation * glm.inverse(self.RotationLocal)
                pose.Scale *= (self.RestPose.Scale / self.ScaleLocal)

        # self alignment
        self.RestPose.Position = self.PositionLocal
        self.RestPose.Rotation = self.RotationLocal
        self.RestPose.Scale = self.ScaleLocal

        # recursion
        if recursive:
            for child in self.Children:
                child.writeRestPose(recursive=True)
        return self

    def readPose(self, frame: int, recursive: bool = True) -> "Joint":
        """Sets the transform position and rotation properties by the given keyframe and rest pose.

        If the frame number is negative, it will look for the n-th frame from the end.

        If recursive, the children do also load their keyframe data."""
        if len(self.Keyframes) == 0: return self
        if frame < 0: frame = max(0, self.KeyframeRange[1] + 1 - frame)

        pose: Pose = None
        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)
        if index == len(self.Keyframes):
            pose = self.Keyframes[-1][1]
        elif self.Keyframes[index][0] != frame:
            if index == 0:
                pose = self.Keyframes[-1][1]
            else:
                weight = (self.Keyframes[index][0] + frame) / self.Keyframes[index + 1][0]
                before = self.Keyframes[index][1]
                after = self.Keyframes[index + 1][1]
                pose = Pose(
                    glm.lerp(before.Position, after.Position, weight),
                    glm.lerp(before.Rotation, after.Rotation, weight),
                    glm.lerp(before.Scale, after.Scale, weight)
                )
        else:
            pose = self.Keyframes[index][1]

        self._CurrentFrame = frame
        self.PositionLocal = self.RestPose.Position + pose.Position
        self.RotationLocal = self.RestPose.Rotation * pose.Rotation
        self.ScaleLocal = self.RestPose.Scale * pose.Scale

        if recursive:
            for child in self.Children:
                child.readPose(frame, recursive=True)

        return self

    def writePose(self, frame: int, recursive: bool = True) -> "Joint":
        """Sets the keyframe properties by the current transform local position and local rotation.

        If the frame number is negative, it will look for the n-th frame from the end.

        If recursive the children do also update their keyframe data."""
        if frame < 0: frame = max(0, self.KeyframeRange[1] + 1 - frame)

        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)
        if index == len(self.Keyframes) or self.Keyframes[index][0] != frame:
            bisect.insort(self.Keyframes, (index, Pose()))

        pose = self.Keyframes[index][1]
        pose.Position = self.PositionLocal - self.RestPose.Position
        pose.Rotation = glm.inverse(self.RestPose.Rotation) * self.RotationLocal
        pose.Scale = self.ScaleLocal / self.RestPose.Scale

        if recursive:
            for child in self.Children:
                child.writePose(frame, recursive=True)

        return self

    def attach(
            self,
            *nodes: "Joint",
            keepPosition: bool = False,
            keepRotation: bool = False,
            keepScale: bool = False,
            updateRestPose: bool = True) -> "Joint":
        for node in nodes:
            if node in self.Children: continue

            # attach the joint
            super().attach(node, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale)

            # apply attach corrections to animation data
            if updateRestPose:
                if keepPosition:
                    parentPoseSpaceWorld = (self.Parent.SpaceWorld if self.Parent else glm.mat4()) * self.RestPose.Space
                    node.RestPose.Position = glm.inverse(parentPoseSpaceWorld) * node.RestPose.Position
                if keepRotation:
                    parentPoseRotationWorld = (self.Parent.SpaceWorld if self.Parent else glm.quat()) * self.RestPose.Rotation
                    node.RestPose.Rotation = glm.inverse(parentPoseRotationWorld) * node.RestPose.Rotation
                if keepScale:
                    parentPoseScaleWorld = (self.Parent.SpaceWorld if self.Parent else glm.quat()) * self.RestPose.Scale
                    node.RestPose.Scale = (1 / parentPoseScaleWorld) * node.RestPose.Scale
        return self

    def detach(
            self,
            *nodes: "Joint",
            keepPosition: bool = False,
            keepRotation: bool = False,
            keepScale: bool = False,
            updateKeyframes: bool = True) -> "Joint":
        for node in nodes:
            if node.Parent is None or node.Parent != self: continue

            # apply detach corrections to animation data
            if updateKeyframes:
                if keepPosition:
                    parentPoseSpaceWorld = (self.Parent.SpaceWorld if self.Parent else glm.mat4()) * self.RestPose.Space
                    node.RestPose.Position = parentPoseSpaceWorld * node.RestPose.Position
                if keepRotation:
                    parentPoseRotationWorld = (self.Parent.SpaceWorld if self.Parent else glm.quat()) * self.RestPose.Rotation
                    node.RestPose.Rotation = parentPoseRotationWorld * node.RestPose.Rotation
                if keepScale:
                    parentPoseScaleWorld = (self.Parent.SpaceWorld if self.Parent else glm.quat()) * self.RestPose.Scale
                    node.RestPose.Scale = parentPoseScaleWorld * node.RestPose.Scale

            # finally detatch the joint
            super().detach(node, keepPosition, keepRotation, keepScale)
        return self

    def clearParent(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False, updateKeyframes: bool = True) -> "Joint":
        return super().clearParent(keepPosition, keepRotation, keepScale, updateKeyframes)

    def clearChildren(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False, updateKeyframes: bool = True) -> "Joint":
        return super().clearChildren(keepPosition, keepRotation, keepScale, updateKeyframes)

    def applyPosition(self, position: glm.vec3 = None, recursive: bool = False, updateKeyframes: bool = True) -> "Joint":
        # define positional change
        change = -self.PositionLocal if position is None else position
        changeInverse = glm.inverse(self.RotationLocal) * (glm.div(1, self.ScaleLocal) * -change)

        # apply to current data
        recursion = recursive and (not updateKeyframes)
        super().applyPosition(position, recursive=recursion, updateKeyframes=updateKeyframes)

        # apply to keyframes
        if updateKeyframes:
            for pose in self._Keyframes:
                pose.Position += change
            for child in self._Children:
                for pose in child._Keyframes:
                    pose.Position += changeInverse

        # may do it recursivly
        if recursive:
            for child in self._Children:
                child.applyPosition(position, recursive=True)

        return self

    def applyRotation(self, rotation: glm.quat = None, recursive: bool = False, updateKeyframes: bool = True) -> "Joint":
        # define rotational change
        change = glm.inverse(self.RotationLocal) if rotation is None else rotation
        changeInverse = glm.inverse(change)

        # apply to current data
        recursion = recursive and (not updateKeyframes)
        super().applyRotation(rotation, recursive=recursion, updateKeyframes=updateKeyframes)

        # apply to keyframes
        if updateKeyframes:
            for pose in self._Keyframes:
                pose.Rotation = change * pose.Rotation
            for child in self._Children:
                for pose in child._Keyframes:
                    pose.Position = changeInverse * pose.Position
                    pose.Rotation = changeInverse * pose.Rotation
                if recursive:
                    child.applyRotation(rotation, recursive=True)

        return self

    def appyScale(self, scale: glm.vec3 = None, recursive: bool = False, updateKeyframes: bool = True) -> "Joint":
        # define change in scale
        changeFrame = glm.div(self.ScaleLocal, self._Keyframes[self._CurrentFrame].Scale)
        change = glm.div(1, self.ScaleLocal) if scale is None else scale
        changeInverse = glm.div(1, change)

        # apply to current data
        recursion = recursive and (not updateKeyframes)
        super().appyScale(scale, recursive=recursion, updateKeyframes=updateKeyframes)

        # apply to keyframes
        if updateKeyframes:
            for pose in self._Keyframes:
                pose.Scale *= changeFrame * change
            for child in self._Children:
                for pose in child._Keyframes:
                    pose.Position *= changeInverse
                    pose.Scale *= changeInverse
                if recursive:
                    child.appyScale(scale, recursive=True)

        return self

    def roll(self, degrees: float, recursive: bool = False, updateKeyframes: bool = True) -> "Joint":
        """Rolls the joint along its local Y axis. Updates the children so there is no spatial change

        Returns itself"""
        change = glm.angleAxis(glm.radians(degrees), (0, 1, 0))
        changeInverse = glm.inverse(change)

        self.RotationLocal = self.RotationLocal * change
        if updateKeyframes:
            for pose in self._Keyframes:
                pose.Rotation = pose.Rotation * change

        for child in self._Children:
            child.PositionLocal = changeInverse * child.PositionLocal
            child.RotationLocal = changeInverse * child.RotationLocal
            if updateKeyframes:
                for pose in child._Keyframes:
                    pose.Position = changeInverse * pose.Position
                    pose.Rotation = changeInverse * pose.Rotation
            if recursive:
                child.roll(degrees, recursive=True)

        return self

    def filter(self, pattern: str, isEqual: bool = False, caseSensitive: bool = False) -> list["Joint"]:
        return super().filter(pattern, isEqual, caseSensitive)

    def filterRegex(self, pattern: str) -> list["Joint"]:
        return super().filterRegex(pattern)

    def layout(self, index: int = 0, depth: int = 0) -> list[tuple["Joint", int, int]]:
        return super().layout(index, depth)
