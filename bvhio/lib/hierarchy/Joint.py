import glm
import bisect
from SpatialTransform import Transform
from ..shared import Pose


class Joint(Transform):

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
    def Keyframes(self) -> list[tuple[int, Pose]]:
        """Animation data for the joint. A keyframe holds the change of local properties in relation to the rest pose, so that Pose = (RestPose + Keyframe).

        The first element in the tuple is the frame id and the second element are the local keyframe properties."""
        return self._Keyframes

    @Keyframes.setter
    def Keyframes(self, value: list[tuple[int, Pose]]) -> None:
        self._Keyframes = list(value)

    @property
    def RestPose(self) -> Pose:
        """Pose without any keyframe applied. The common T-Pose would go here. This Pose is the base for all animation data."""
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
        """Sets joint properties to the rest pose.

        If recursive is True -> Child joints do also load their rest pose.

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

    def writeRestPose(self, recursive: bool = True, updateKeyframes: bool = False) -> "Joint":
        """Sets the rest pose to the current joint properties.

        If updateKeyframes is True -> Keyframes are modified so that the animation
        (NewRestPose + Keyframe) does not change.

        Returns itself."""
        # keyframe update
        if updateKeyframes:
            for frame, pose in self.Keyframes:
                pose.Position = pose.Position + (self.RestPose.Position - self.PositionLocal)
                pose.Rotation = pose.Rotation * (self.RestPose.Rotation * glm.inverse(self.RotationLocal))
                pose.Scale = pose.Scale * (self.RestPose.Scale / self.ScaleLocal)

        # write rest pose
        self.RestPose.Position = self.PositionLocal
        self.RestPose.Rotation = self.RotationLocal
        self.RestPose.Scale = self.ScaleLocal

        # recursion
        if recursive:
            for child in self.Children:
                child.writeRestPose(recursive=True)

        return self

    def readPose(self, frame: int, recursive: bool = True) -> "Joint":
        """Sets joint properties to the pose at the given frame id. The pose is defined by (RestPose + Keyframe).

        If the frame number is negative, it will look for the n-th frame from the end.

        If there are no keyframes, the joint propetries will not change.

        If the frame id is out of the keyframe length, the nearest keyframe propetires are used.

        If the frame id is between two keyframes, the pose properties are linearly interpolated.

        If recursive is True -> Child joints do also load their pose.

        Returns itself."""
        if len(self.Keyframes) == 0: return self
        if frame < 0: frame = max(0, self.getKeyframeRange(includeChildren=False)[1] + 1 - frame)

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
        """Sets joint properties as pose for the given frame id.

        The keyframe data is calculated so that Pose = (RestPose + Keyframe).

        If the frame number is negative, it counts as the n-th frame from the end.

        If recursive is True -> Child joints do also write their pose.

        Returns itself."""
        if frame < 0: frame = max(0, self.getKeyframeRange(includeChildren=False)[1] + 1 - frame)

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

    def getKeyframeRange(self, includeChildren: bool = False) -> tuple[int, int]:
        """Returns the earliest and latest frame id of the animation.

        If includeChildren is True -> The range considers the earliest and latest frames from its children too."""
        range = (self.Keyframes[0][0], self.Keyframes[-1][0])

        if includeChildren:
            for child in self.Children:
                childRange = child.getKeyframeRange(includeChildren=True)
                range[0] = min(range[0], childRange[0])
                range[1] = max(range[1], childRange[1])

        return range

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
            updateRestPose: bool = True) -> "Joint":
        for node in nodes:
            if node.Parent is None or node.Parent != self: continue

            # apply detach corrections to animation data
            if updateRestPose:
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

    def roll(self, degrees: float, recursive: bool = False) -> "Joint":
        """Rotates the joint along its local Y axis and updates the children so there is no spatial change.

        RestPose and Keyframe data are not modified. If you want to roll them consider to use -> joint.readPose().roll().writePose().

        Returns itself.
        """
        change = glm.angleAxis(glm.radians(degrees), (0, 1, 0))
        changeInverse = glm.inverse(change)

        self.RotationLocal = self.RotationLocal * change
        for child in self._Children:
            child.PositionLocal = changeInverse * child.PositionLocal
            child.RotationLocal = changeInverse * child.RotationLocal

            if recursive:
                child.roll(degrees, recursive=True)

        return self

    def clearParent(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False, updateRestPose: bool = True) -> "Joint":
        if self.Parent is not None:
            self.Parent.detach(self, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale, updateRestPose=updateRestPose)
        return self

    def clearChildren(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False, updateRestPose: bool = True) -> "Joint":
        if len(self.Children) > 0:
            self.detach(*self.Children, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale, updateRestPose=updateRestPose)
        return self

    def applyPosition(self, position: glm.vec3 = None, recursive: bool = False) -> "Joint":
        return super().applyPosition(position, recursive)

    def applyRotation(self, rotation: glm.quat = None, recursive: bool = False) -> "Joint":
        return super().applyRotation(rotation, recursive)

    def appyScale(self, scale: glm.vec3 = None, recursive: bool = False) -> "Joint":
        return super().appyScale(scale, recursive)

    def filter(self, pattern: str, isEqual: bool = False, caseSensitive: bool = False) -> list["Joint"]:
        return super().filter(pattern, isEqual, caseSensitive)

    def filterRegex(self, pattern: str) -> list["Joint"]:
        return super().filterRegex(pattern)

    def layout(self, index: int = 0, depth: int = 0) -> list[tuple["Joint", int, int]]:
        return super().layout(index, depth)
