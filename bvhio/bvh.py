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

    def __init__(self, position:glm.vec3 = glm.vec3(), Rotation:glm.quat = glm.quat()) -> None:
        self._Position = glm.vec3(position)
        self._Rotation = glm.quat(Rotation)

    def __repr__(self) -> str:
        return (f"Pos: {self.Position}, Rot: {self.Rotation}")

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

    def getTip(self) -> glm.vec3:
        """Calculates the tip of the defined bone.

        The tip position is the average position of all children in local space without rotation.
        If there is no child joint, the EndSite value will be returned."""
        children = len(self.Children)
        if children == 1: return self.Children[0].Offset
        elif children > 1: return sum(child.Offset for child in self.Children) / children
        else: return self.EndSite

    def getLength(self) -> float:
        """Length of the bone which is based on the tip."""
        return glm.length(self.getTip())

    def getRotation(self) -> glm.quat:
        """calculate the bone rotation based on the tip."""
        tipDir = glm.normalize(self.getTip())
        tipAxis = glm.vec3(0, 0, 1)
        tipDot = glm.abs(glm.dot(tipDir, tipAxis))
        if tipDot > 0.999: tipAxis = glm.vec3(1, 0, 0)
        return glm.quatLookAtRH(tipDir, tipAxis)

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
    def Keyframes(self) -> list[Pose]: return self._Keyframes
    @Keyframes.setter
    def Keyframes(self, value:list[Pose]) -> None: self._Keyframes = list(value)

    def __init__(self, name:str, position:glm.vec3 = glm.vec3(), rotation:glm.quat = glm.quat(), scale:glm.vec3 = glm.vec3(1)) -> None:
        super().__init__(name, position, rotation)
        self._Keyframes:list[Pose] = []

    def readPose(self, frame:int, recursive: bool = True) -> "Joint":
        """Sets the transform position and rotation properties by the given keyframe.

        If recursive the children do also load their keyframe data."""
        if frame < 0 or frame >= len(self._Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self._Keyframes)} Keyframes)')
        self.Position = self._Keyframes[frame].Position
        self.Rotation = self._Keyframes[frame].Rotation

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
        elif frame == len(self._Keyframes):
            self._Keyframes.append(Pose(self.Position, self.Rotation))

        if recursive:
            for child in self.Children:
                child.writePose(frame)
        return self

    def attach(self, *nodes: "Joint", keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        for node in nodes:
            # attach the joint
            super().attach(node, keepPosition=keepPosition, keepRotation=keepRotation, keepScale=keepScale)

            # apply attach corrections to animation data
            for pose in node.Keyframes:
                if keepPosition: pose.Position = self.pointToLocal(pose.Position)
                if keepRotation: pose.Rotation = pose.Rotation * (glm.inverse(self.Rotation))
        return self

    def detach(self, node: "Joint", keepPosition: bool = False, keepRotation: bool = False, keepScale: bool = False) -> "Joint":
        # apply detach corrections to animation data
        for pose in node._Keyframes:
            if keepPosition: pose.Position = self.pointToWorld(node.Position)
            if keepRotation: pose.Rotation = pose.Rotation * self.Rotation

        # finally detatch the joint
        return super().detach(node, keepPosition, keepRotation, keepScale)

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
