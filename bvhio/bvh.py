import numpy
import glm
import SpatialTransform as tr


class Keyframe:
    @property
    def Position(self) -> glm.vec3:
        return self._Position
    @Position.setter
    def Position(self, value:glm.vec3) -> None:
        self._Position = glm.vec3(value)

    @property
    def Orientation(self) -> glm.quat:
        return self._Orientation
    @Orientation.setter
    def Orientation(self, value:glm.quat) -> None:
        self._Orientation = glm.quat(value)

    def __init__(self, position:glm.vec3 = glm.vec3(), orientation:glm.quat = glm.quat()) -> None:
        self._Position = glm.vec3(position)
        self._Orientation = glm.quat(orientation)

class Joint(tr.Transform):
    Bone:Keyframe
    Keyframes:list[Keyframe]
    Channels:list[str]

    @property
    def Tip(self) -> glm.vec3:
        children = len(self.Children)
        if children == 1: return self.Children[0].Position
        elif children > 1: return sum(child.Position for child in self.Children) / children
        else: return self._Tip
    @Tip.setter
    def Tip(self, value:glm.vec3) -> None:
        self._Tip = glm.vec3(value) if value is not None and glm.length(value) > 0.001 else glm.vec3(0, 1, 0)

    @property
    def Length(self) -> float:
        return glm.length(self.Tip)

    def __init__(self, name:str) -> None:
        super().__init__()
        self.Name = name
        self.Bone = Keyframe()
        self.Channels = []
        self.Keyframes = []
        self.Tip = glm.vec3()

    def layout(self) -> list[object]:
        result = [self]
        for child in self.Children:
            result.extend(child.layout())
        return result

    def readBone(self, recursive: bool = True) -> None:
        self.Position = self.Bone.Position
        self.Orientation = self.Bone.Orientation
        if recursive:
            for child in self.Children: child.readBone(recursive)

    def writeBone(self, recursive: bool = True) -> None:
        if recursive:
            for child in self.Children: child.writeBone(recursive)

    def readPose(self, frame:int, recursive: bool = True) -> None:
        self.Position = self.Keyframes[frame].Position
        self.Orientation = self.Keyframes[frame].Orientation
        if recursive:
            for child in self.Children: child.readPose(frame)

    def writePose(self, frame:int, recursive: bool = True) -> None:
        self.Keyframes[frame].Position = self.Position
        self.Keyframes[frame].Orientation = self.Orientation
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
