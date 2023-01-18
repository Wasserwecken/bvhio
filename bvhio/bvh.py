import glm
from SpatialTransform import Transform

class Pose:
    """Data structure for holding pose data."""

    @property
    def Position(self) -> glm.vec3: return glm.vec3(self._Position)
    @Position.setter
    def Position(self, value:glm.vec3) -> None: self._Position = glm.vec3(value)

    @property
    def Rotation(self) -> glm.quat: return glm.quat(self._Rotation)
    @Rotation.setter
    def Rotation(self, value:glm.quat) -> None: self._Rotation = glm.quat(value)

    @property
    def Scale(self) -> glm.vec3: return glm.vec3(self._Scale)
    @Scale.setter
    def Scale(self, value:glm.vec3) -> None: self._Scale = glm.vec3(value)

    def __init__(self, position:glm.vec3 = glm.vec3(), rotation:glm.quat = glm.quat(), scale:glm.vec3 = glm.vec3(1)) -> None:
        self._Position = glm.vec3(position)
        self._Rotation = glm.quat(rotation)
        self._Scale = glm.vec3(scale)

    def __repr__(self) -> str:
        return (f"Pos: {self.Position}, Rot: {self.Rotation}, Scale: {self.Scale}")

    def __str__(self) -> str:
        return self.__repr__()

class RootPose:
    """Data structure for the bvh skeleton definition. Contains the attributes as in the BVH file.

    Keyframes contain the motion data."""
    Name:str
    Offset:glm.vec3
    EndSite:glm.vec3
    Keyframes:list[Pose]
    Channels:list[str]
    Children:list["RootPose"]

    def __init__(self, name:str, offset: glm.vec3 = glm.vec3()) -> None:
        self.Name = name
        self.Offset = offset
        self.EndSite = glm.vec3(0,1,0)
        self.Keyframes = []
        self.Channels = []
        self.Children = []

    def __repr__(self) -> str:
        return (f"{self.Name}")

    def __str__(self) -> str:
        return self.__repr__()

    def getTip(self) -> glm.vec3:
        """Calculates the tip of the defined bone.

        The tip position is the average position of all children in local space without rotation.
        If there is no child joint, the EndSite value will be returned."""
        children = len(self.Children)
        if children == 1: return self.Children[0].Offset
        elif children > 1: return sum(child.Offset for child in self.Children) / children
        else: return self.EndSite if glm.length(self.EndSite) > 0.001 else glm.vec3(0,1,0)

    def getLength(self) -> float:
        """Length of the bone which is based on the tip."""
        return glm.length(self.getTip())

    def getRotation(self) -> glm.quat:
        """calculate the bone rotation based on the tip."""
        # https://arrowinmyknee.com/2021/02/10/how-to-get-rotation-from-two-vectors/
        dir = glm.normalize(self.getTip())
        axis = glm.vec3(0, 1, 0)
        dot = glm.dot(axis, dir)

        if dot < -0.999: return glm.quat(0,0,0,1)
        return glm.angleAxis(glm.acos(dot), glm.cross(axis, dir))

    def layout(self, index:int = 0, depth:int = 0) -> list[tuple["RootPose", int, int]]:
        """Returns the hierarchical layout of this joint and its children recursivly."""
        result = [[self, index, depth]]
        for child in self.Children:
            result.extend(child.layout(result[-1][1] + 1, depth + 1))
        return result


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
    def Keyframes(self, value:list[Pose]) -> None: self._Keyframes = list(value)

    def __init__(self, name:str, position:glm.vec3 = glm.vec3(), rotation:glm.quat = glm.quat(), scale:glm.vec3 = glm.vec3(1)) -> None:
        super().__init__(name, position, rotation, scale)
        self._Keyframes:list[Pose] = []
        self._Parent:"Joint" = None
        self._Children:list["Joint"] = []
        self._CurrentFrame = -1

    def readPose(self, frame:int, recursive: bool = True) -> "Joint":
        """Sets the transform position and rotation properties by the given keyframe.

        If recursive the children do also load their keyframe data."""
        if frame < 0 or frame >= len(self._Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self._Keyframes)} Keyframes)')

        self._CurrentFrame = frame
        self.Position = self._Keyframes[frame].Position
        self.Rotation = self._Keyframes[frame].Rotation
        self.Scale = self._Keyframes[frame].Scale

        if recursive:
            for child in self.Children:
                child.readPose(frame, recursive)
        return self

    def writePose(self, frame:int, recursive: bool = True) -> "Joint":
        """Sets the keyframe properties by the current transform local position and local rotation.

        If recursive the children do also update their keyframe data."""
        if frame < 0 or frame > len(self._Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range.')

        elif frame < len(self._Keyframes):
            self._Keyframes[frame].Position = self.Position
            self._Keyframes[frame].Rotation = self.Rotation
            self._Keyframes[frame].Scale = self.Scale

        elif frame == len(self._Keyframes):
            self._Keyframes.append(Pose(self.Position, self.Rotation))

        if recursive:
            for child in self.Children:
                child.writePose(frame)
        return self

    def attach(self, *nodes: "Joint", keepPosition: bool = True, keepRotation: bool = True, keepScale: bool = True) -> "Joint":
        _, wsRotation, wsScale, _, _ = self.decomposeSpaceWorldInverse()
        for node in nodes:
            # attach the joint
            super().attach(node, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale)

            # apply attach corrections to animation data
            for pose in node.Keyframes:
                if keepPosition: pose.Position = self.SpaceWorldInverse * pose.Position
                if keepRotation: pose.Rotation = wsRotation * pose.Rotation
                if keepScale: pose.Scale = wsScale * pose.Scale
        return self

    def detach(self, node: "Joint", keepPosition: bool = True, keepRotation: bool = True, keepScale: bool = True) -> "Joint":
        _, wsRotation, wsScale, _, _ = self.decomposeSpaceWorld()

        # apply detach corrections to animation data
        for pose in node._Keyframes:
            if keepPosition: pose.Position = self.SpaceWorld * pose.Position
            if keepRotation: pose.Rotation = wsRotation * pose.Rotation
            if keepScale: pose.Scale = wsScale * pose.Scale

        # finally detatch the joint
        return super().detach(node, keepPosition, keepRotation, keepScale)


    def clearParent(self, keepPosition: bool = True, keepRotation: bool = True, keepScale: bool = True) -> "Joint":
        return super().clearParent(keepPosition, keepRotation, keepScale)

    def clearChildren(self, keepPosition: bool = True, keepRotation: bool = True, keepScale: bool = True) -> "Joint":
        return super().clearChildren(keepPosition, keepRotation, keepScale)


    def applyPosition(self, position:glm.vec3 = glm.vec3()) -> "Joint":
        change = self.Position + position
        super().applyPosition(position)

        for pose in self._Keyframes:
            pose.Position = -change + pose.Rotation
        for child in self._Children:
            for pose in child._Keyframes:
                pose.Position = change + pose.Position

        return self

    def applyRotation(self, rotation:glm.quat = glm.quat(), recursive:bool = False, includeLocal:bool = False) -> "Joint":
        change = rotation * self.Rotation
        super().applyRotation(rotation, recursive=False, includeLocal=includeLocal)

        for pose in self._Keyframes:
            pose.Rotation = glm.inverse(change) * pose.Rotation
            if includeLocal:
                pose.Position = change * pose.Position
        for child in self._Children:
            for pose in child._Keyframes:
                pose.Position = change * pose.Position
                pose.Rotation = change * pose.Rotation
            if recursive:
                child.applyRotation(recursive=True, includeLocal=False)

        return self

    def appyScale(self, scale:glm.vec3 = glm.vec3(1), recursive:bool = False, includeLocal:bool = False) -> "Joint":
        change = self.Scale * scale
        super().appyScale(scale, recursive=False, includeLocal=includeLocal)

        for pose in self._Keyframes:
            pose.Scale *= glm.div(scale, change)
            if includeLocal:
                pose.Position *= change
        for child in self._Children:
            for pose in child._Keyframes:
                pose.Position *= change
                pose.Scale *= change
            if recursive:
                child.appyScale(recursive=True, includeLocal=False)

        return self

    def filter(self, pattern:str, isEqual:bool = False, caseSensitive: bool = False) -> list["Joint"]:
        return super().filter(pattern, isEqual, caseSensitive)

    def filterRegex(self, pattern: str) -> list["Joint"]:
        return super().filterRegex(pattern)

    def layout(self, index: int = 0, depth: int = 0) -> list[tuple["Joint", int, int]]:
        return super().layout(index, depth)


class BVH:
    """Container for the information of the bvh file.

    Root is the recursive definition of the skeleton.

    Frame time the frame time.

    Frams are the count of keyframes of the motion."""
    Root:RootPose
    FrameTime:float
    FrameCount:int

    def __init__(self):
        self.Hierarchy = None
        self.FrameTime = None
        self.FrameCount = None
