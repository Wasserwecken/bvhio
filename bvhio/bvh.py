import glm
from SpatialTransform import Transform

class Pose:
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
        children = len(self.Children)
        if children == 1: return self.Children[0].Position
        elif children > 1: return sum(child.Position for child in self.Children) / children
        else: return defaultTip if glm.length(defaultTip) > 0.01 else glm.vec3(0,1,0)

    def getLength(self) -> float:
        return glm.length(self.GetTip())

    def layout(self, index:int = 0, depth:int = 0) -> list[tuple["RootPose", int, int]]:
        result = [[self, index, depth]]
        for child in self.Children:
            result.extend(child.layout(result[-1][1] + 1, depth + 1))
        return result


class Joint(Transform):
    DataBVH:RootPose
    Keyframes:list[Pose]

    def __init__(self, dataBVH:RootPose) -> None:
        super().__init__(dataBVH.Name, dataBVH.Position, dataBVH.Rotation)
        self.Keyframes = []
        self.DataBVH = dataBVH
        for childData in dataBVH.Children:
            self.attach(Joint(childData))

    def readPose(self, frame:int, recursive: bool = True, fromBVH:bool = False) -> "Joint":
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
    Hierarchy:Joint
    FrameTime:float

    def __init__(self):
        self.Hierarchy = None
        self.FrameTime = None

    @property
    def Frames(self) -> float:
        return len(self.Hierarchy.Keyframes) if self.Hierarchy is not None else 0
