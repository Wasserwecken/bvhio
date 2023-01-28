import glm
import bisect
from SpatialTransform import Transform
from ..shared import Pose


class Joint(Transform):
    """Spatial definition of an linear space with position, rotation and scale.

    - Bone alignment is expected to be along the Y+ axis.
    - Space is defined as right handed where Y+:up and X+:right and Z-:forward.
    - Positive rotations are counter clockwise."""

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
        """Animation data for the joint. A keyframe holds the change of local properties in relation to the rest pose, so that 'Pose = RestPose + Keyframe'.

    - The first element in the tuple is the frame id and the second element are the local keyframe properties.
    - This is an ordered list by the frame id. Please do not change this manually, unless you know what your doing.
    - Negative frame ids cannot exist."""
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

        - If recursive is True -> Child joints do also load their rest pose.

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

        - If updateKeyframes is False -> The keyframes do not change. The animation itself will change.
        - If updateKeyframes is True -> The keyframes are modified, so that the animation itself 'Pose = RestPose + Keyframe' does not change.

        Returns itself."""
        # remove change in rest pose from keyframes
        if updateKeyframes:
            for frame, key in self.Keyframes:
                key.Position = key.Position + (self.RestPose.Position - self.PositionLocal)
                key.Rotation = key.Rotation * (self.RestPose.Rotation * glm.inverse(self.RotationLocal))
                key.Scale = key.Scale * (self.RestPose.Scale / self.ScaleLocal)

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
        """Sets joint properties to the animation at the given frame id. The animation is defined as 'Pose = RestPose + Keyframe'.

        - If the frame number is negative, it will look for the n-th frame from the end.
        - If there are no keyframes, the joint propetries will not change.
        - If the frame id is out of the keyframe length, the nearest keyframe propetires are used.
        - If the frame id is between two keyframes, pose properties are linearly interpolated.
        - If recursive is True -> Child joints do also load their pose.

        Returns itself."""
        if len(self.Keyframes) == 0: return self
        if frame < 0: frame = max(0, self.getKeyframeRange(includeChildren=False)[1] + 1 - frame)

        key: Pose = None
        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)
        if index == len(self.Keyframes):
            key = self.Keyframes[-1][1]  # index is bigger than last frame, take last key
        elif self.Keyframes[index][0] != frame:
            if index == 0:
                key = self.Keyframes[-1][1]  # index is smaller than first frame, take first key
            else:
                # index is in between two keyframes, interpolate
                weight = (self.Keyframes[index][0] + frame) / self.Keyframes[index + 1][0]
                before = self.Keyframes[index][1]
                after = self.Keyframes[index + 1][1]
                key = Pose(
                    glm.lerp(before.Position, after.Position, weight),
                    glm.lerp(before.Rotation, after.Rotation, weight),
                    glm.lerp(before.Scale, after.Scale, weight)
                )
        else:
            key = self.Keyframes[index][1]  # index mathces a keyframe

        # calculate animation pose
        self._CurrentFrame = frame
        self.PositionLocal = self.RestPose.Position + key.Position
        self.RotationLocal = self.RestPose.Rotation * key.Rotation
        self.ScaleLocal = self.RestPose.Scale * key.Scale

        # may do it recursively
        if recursive:
            for child in self.Children:
                child.readPose(frame, recursive=True)

        return self

    def writePose(self, frame: int, recursive: bool = True, updateRestpose: bool = False) -> "Joint":
        """Sets joint properties as animation pose for the given frame id.

        - If the frame number is negative, it counts as the n-th frame from the end.
        - If recursive is True -> Child joints do also write their pose.
        - If updateRestpose is False -> The rest pose does not change, the keyframe is calculated so that 'Keyframe = Pose - RestPose'.
        - If updateRestpose is True -> The keyframe does not change, the rest pose is calculated so that 'Restpose = Pose - Keyframe'.

        Returns itself."""
        if frame < 0: frame = max(0, self.getKeyframeRange(includeChildren=False)[1] + 1 - frame)

        # binary search, creates key if not exists
        index = bisect.bisect_left([key[0] for key in self.Keyframes], frame)
        if index == len(self.Keyframes) or self.Keyframes[index][0] != frame:
            bisect.insort(self.Keyframes, (index, Pose()))
        key = self.Keyframes[index][1]

        if updateRestpose:
            self.RestPose.Position = self.PositionLocal - key.Position
            self.RestPose.Rotation = glm.inverse(key.Rotation) * self.RotationLocal
            self.RestPose.Scale = self.ScaleLocal / key.Scale
        else:
            key.Position = self.PositionLocal - self.RestPose.Position
            key.Rotation = glm.inverse(self.RestPose.Rotation) * self.RotationLocal
            key.Scale = self.ScaleLocal / self.RestPose.Scale

        if recursive:
            for child in self.Children:
                child.writePose(frame, recursive=True)

        return self

    def getKeyframeRange(self, includeChildren: bool = False) -> tuple[int, int]:
        """Returns the earliest and latest frame id of the animation.

        - If includeChildren is True -> The range considers the earliest and latest frames from its children too.

        The tuple layout is -> [FirstFrameId, LastFrameId]"""
        range = (self.Keyframes[0][0], self.Keyframes[-1][0])

        if includeChildren:
            for child in self.Children:
                childRange = child.getKeyframeRange(includeChildren=True)
                range[0] = min(range[0], childRange[0])
                range[1] = max(range[1], childRange[1])

        return range

    def roll(self, degrees: float, recursive: bool = False) -> "Joint":
        """Rotates the joint along its local Y axis and updates the children so there is no spatial change.

        - RestPose and Keyframe data are not modified. If you want to roll them consider to use -> joint.readPose().roll().writePose().

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

    def attach(self, *nodes: "Joint", keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        return super().attach(*nodes, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale)

    def detach(self, *nodes: "Joint", keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        return super().detach(*nodes, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale)

    def clearParent(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        return super().clearParent(keepPosition, keepRotation, keepScale)

    def clearChildren(self, keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        return super().clearChildren(keepPosition, keepRotation, keepScale)

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
