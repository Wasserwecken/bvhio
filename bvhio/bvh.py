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

    def __init__(self, name:str, position:glm.vec3 = glm.vec3(), rotation:glm.quat = glm.quat(), scale:glm.vec3 = glm.vec3(1), keyframePlaceholders:int = 0) -> None:
        super().__init__(name, position, rotation, scale)
        self._Parent:"Joint" = None
        self._Children:list["Joint"] = []

        if keyframePlaceholders == 0:
            self._Keyframes:list[Pose] = []
            self._CurrentFrame = -1
        else:
            self._Keyframes:list[Pose] = [Pose() for _ in range(keyframePlaceholders)]
            self.readPose(0)


    def readPose(self, frame:int, recursive: bool = True) -> "Joint":
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

    def writePose(self, frame:int, recursive: bool = True) -> "Joint":
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


    def applyPosition(self, position:glm.vec3 = None, recursive:bool = False) -> "Joint":
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

    def applyRotation(self, rotation:glm.quat = None, recursive:bool = False) -> "Joint":
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

    def appyScale(self, scale:glm.vec3 = None, recursive:bool = False) -> "Joint":
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

    def roll(self, degrees:float, recursive:bool = False) -> "Joint":
        """Rolls the joint along its local Y axis. Updates the children so there is no spatial change

        Returns itself"""
        change = glm.angleAxis(glm.radians(degrees), (0,1,0))
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
        self.Root:RootPose = None
        self.FrameTime:float = None
        self.FrameCount:int = None
