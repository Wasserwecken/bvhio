import glm
from SpatialTransform import Transform

class Pose:
    """Data strcture for holding transform data. Used for keyframes and internal parsing."""
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

class RootPose(Pose):
    """Data structure for the bvh skeleton definition. Not aware about parent spaces.

    The position is in local space without rotation.

    The rotation is defined by the position, rotated along the Z axis.

    The keyframes are the motion data."""
    Name:str
    Keyframes:list[Pose]
    Channels:list[str]
    Children:list["RootPose"]

    def __init__(self, name:str = '', position: glm.vec3 = glm.vec3(), Rotation: glm.quat = glm.quat()) -> None:
        super().__init__(position, Rotation)
        self.Name = name
        self.Keyframes = []
        self.Channels = []
        self.Children = []

    def __repr__(self) -> str:
        return (f"Name: {self.Name}, Pos: {self.Position}, Rot: {self.Rotation}")

    def getTip(self, defaultTip:glm.vec3 = glm.vec3()) -> glm.vec3:
        """Calculates the tip of the defined bone.

        The tip position is the average position of all children in local space without rotation.
        If there is not child joint, the tip position can be set manualy or defaults to (0,1,0)."""
        children = len(self.Children)
        if children == 1: return self.Children[0].Position
        elif children > 1: return sum(child.Position for child in self.Children) / children
        else: return defaultTip if glm.length(defaultTip) > 0.01 else glm.vec3(0,1,0)

    def getLength(self) -> float:
        """Length of the bone which is based on the tip."""
        return glm.length(self.GetTip())

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

    DataBVH:RootPose
    Keyframes:list[Pose]

    def __init__(self, dataBVH:RootPose) -> None:
        super().__init__(dataBVH.Name, dataBVH.Position, dataBVH.Rotation)
        self.Keyframes = []
        self.DataBVH = dataBVH
        for childData in dataBVH.Children:
            self.attach(Joint(childData))

    def readPose(self, frame:int, recursive: bool = True, fromBVH:bool = False) -> "Joint":
        """Sets the transform position and rotation properties by the given keyframe.

        If recursive the children do also load their keyframe data.

        If fomBVH the data from DataBVH is used to set the properties."""
        if fromBVH:
            if frame < 0 or frame >= len(self.DataBVH.Keyframes):
                raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self.DataBVH.Keyframes)} Keyframes)')
            self.Position = self.DataBVH.Keyframes[frame].Position
            self.Rotation = self.DataBVH.Keyframes[frame].Rotation
        else:
            if frame < 0 or frame >= len(self.Keyframes):
                raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self.Keyframes)} Keyframes)')
            self.Position = self.Keyframes[frame].Position
            self.Rotation = self.Keyframes[frame].Rotation

        if recursive:
            for child in self.Children: child.readPose(frame, recursive, fromBVH)

        return self

    def writePose(self, frame:int, recursive: bool = True) -> "Joint":
        """Sets the keyframe properties by the current transform local position and local rotation.

        If recursive the children do also update their keyframe data."""
        if frame < 0 or frame > len(self.Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range.')

        elif frame < len(self.Keyframes):
            self.Keyframes[frame].Position = self.Position
            self.Keyframes[frame].Rotation = self.Rotation
        elif frame == len(self.Keyframes):
            self.Keyframes.append(Pose(self.Position, self.Rotation))

        if recursive:
            for child in self.Children: child.writePose(frame)

        return self

class BVH:
    """Container for the information of the bvh file.

    Hierarchy is the definition of the skeleton.

    Frame time the frame time.

    Frams are the count of keyframes of the motion."""
    Hierarchy:Joint
    FrameTime:float

    def __init__(self):
        self.Hierarchy = None
        self.FrameTime = None

    @property
    def Frames(self) -> float:
        return len(self.Hierarchy.Keyframes) if self.Hierarchy is not None else 0
