import numpy
import glm
import SpatialTransform as st

class Pose:
    @property
    def Position(self) -> glm.vec3: return glm.vec3(self._Position)
    @Position.setter
    def Position(self, value:glm.vec3) -> None: self._Position = glm.vec3(value)

    @property
    def Orientation(self) -> glm.quat: return glm.quat(self._Orientation)
    @Orientation.setter
    def Orientation(self, value:glm.quat) -> None: self._Orientation = glm.quat(value)

    def __init__(self, position:glm.vec3 = glm.vec3(), orientation:glm.quat = glm.quat()) -> None:
        self._Position = glm.vec3(position)
        self._Orientation = glm.quat(orientation)

    def __repr__(self) -> str:
        return (f"Pos: {self.Position}, Rot: {self.Orientation}")

class RootPose(Pose):
    Name:str
    Keyframes:list[Pose]
    Channels:list[str]
    Children:list[object]

    def __init__(self, name:str = '', position: glm.vec3 = glm.vec3(), orientation: glm.quat = glm.quat()) -> None:
        super().__init__(position, orientation)
        self.Name = name
        self.Keyframes = []
        self.Channels = []
        self.Children = []

    def __repr__(self) -> str:
        return (f"Name: {self.Name}, Pos: {self.Position}, Rot: {self.Orientation}")

    def getTip(self, defaultTip:glm.vec3 = glm.vec3()) -> glm.vec3:
        children = len(self.Children)
        if children == 1: return self.Children[0].Position
        elif children > 1: return sum(child.Position for child in self.Children) / children
        else: return defaultTip if glm.length(defaultTip) > 0.01 else glm.vec3(0,1,0)

    def getLength(self) -> float:
        return glm.length(self.GetTip())

    def layout(self, index:int = 0, depth:int = 0) -> list[tuple[object, int, int]]:
        result = [[self, index, depth]]
        for child in self.Children:
            result.extend(child.layout(result[-1][1] + 1, depth + 1))
        return result


class Joint(st.Transform):
    DataBVH:RootPose
    Keyframes:list[Pose]

    def __init__(self, dataBVH:RootPose) -> None:
        super().__init__(dataBVH.Name, dataBVH.Position, dataBVH.Orientation)
        self.Keyframes = []
        self.DataBVH = dataBVH
        for childData in dataBVH.Children:
            self.append(Joint(childData))

    def readPose(self, frame:int, recursive: bool = True, fromBVH:bool = False) -> None:
        if fromBVH:
            if frame < 0 or frame >= len(self.DataBVH.Keyframes):
                raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self.DataBVH.Keyframes)} Keyframes)')
            self.Position = self.DataBVH.Keyframes[frame].Position
            self.Orientation = self.DataBVH.Keyframes[frame].Orientation
        else:
            if frame < 0 or frame >= len(self.Keyframes):
                raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range. ({len(self.Keyframes)} Keyframes)')
            self.Position = self.Keyframes[frame].Position
            self.Orientation = self.Keyframes[frame].Orientation

        if recursive:
            for child in self.Children: child.readPose(frame, recursive, fromBVH)

    def writePose(self, frame:int, recursive: bool = True) -> None:
        if frame < 0 or frame > len(self.Keyframes):
            raise ValueError(f'Frame number "{frame}" for {self.Name} is out of range.')

        elif frame < len(self.Keyframes):
            self.Keyframes[frame].Position = self.Position
            self.Keyframes[frame].Orientation = self.Orientation
        elif frame == len(self.Keyframes):
            self.Keyframes.append(Pose(self.Position, self.Orientation))

        if recursive:
            for child in self.Children: child.writePose(frame)

class BVH:
    Hierarchy:Joint
    FrameTime:float

    def __init__(self):
        self.Hierarchy = None
        self.FrameTime = None

    @property
    def Frames(self) -> float:
        return len(self.Hierarchy.Keyframes) if self.Hierarchy is not None else 0

    @property
    def Motion(self) -> numpy.ndarray:
        layout = self.Hierarchy.layout(0)
        result = layout[0][0].serializeMotion()
        for i in range(1, len(layout)):
            result = numpy.append(result, layout[i][0].serializeMotion(), 1)
        return result

    def layout(self) -> list[tuple[object, int, int]]:
        result = []
        startIndex = 0
        for joint in self.Hierarchy.layout():
            result.append((joint, startIndex, startIndex + len(joint.Channels)))
            startIndex += len(joint.Channels)
        return result
