import numpy
import glm
from .transform import *
from .angles import *

class Joint(Transform):
    Motion:numpy.ndarray
    Channels:list[str]

    def __init__(self, name:str) -> None:
        super().__init__()
        self.Name = name
        self.Channels = []

    def layout(self, startIndex:int = 0) -> list[tuple[object, int, int]]:
        endIndex = startIndex+len(self.Channels)
        result = [[self, startIndex, endIndex]]

        for child in self.Children:
            result.extend(child.layout(result[-1][2]))
        return result

    def serialize(self) -> numpy.ndarray:
        result:list[int] = []

        rotation = glm.vec3()
        rotCurrent = self.Orientation
        rotOrder = [rot[0] for rot in reversed(self.Channels) if rot[1:] == 'rotation']
        for axis in rotOrder:
            if axis == 'X': rotation.x = glm.eulerAngles(rotCurrent).x; rotCurrent = glm.rotate(rotCurrent, -rotation.x, (1.0, 0.0, 0.0)); continue
            if axis == 'Y': rotation.y = glm.eulerAngles(rotCurrent).y; rotCurrent = glm.rotate(rotCurrent, -rotation.y, (0.0, 1.0, 0.0)); continue
            if axis == 'Z': rotation.z = glm.eulerAngles(rotCurrent).z; rotCurrent = glm.rotate(rotCurrent, -rotation.z, (0.0, 0.0, 1.0)); continue
        for channel in self.Channels:
            if 'Xposition' == channel: result.append(self.Position.x); continue
            if 'Yposition' == channel: result.append(self.Position.y); continue
            if 'Zposition' == channel: result.append(self.Position.z); continue
            if 'Xrotation' == channel: result.append(glm.degrees(rotation.x)); continue
            if 'Yrotation' == channel: result.append(glm.degrees(rotation.y)); continue
            if 'Zrotation' == channel: result.append(glm.degrees(rotation.z)); continue
        return numpy.array(result)

    def deserialize(self, data:numpy.ndarray) -> None:
        self.Orientation = glm.quat()
        for (index, channel) in enumerate(self.Channels):
            if 'Xposition' == channel: self.Position.x = data[index]; continue
            if 'Yposition' == channel: self.Position.y = data[index]; continue
            if 'Zposition' == channel: self.Position.z = data[index]; continue
            if 'Xrotation' == channel: self.Orientation = glm.rotate(self.Orientation, glm.radians(data[index]), (1.0, 0.0, 0.0)); continue
            if 'Yrotation' == channel: self.Orientation = glm.rotate(self.Orientation, glm.radians(data[index]), (0.0, 1.0, 0.0)); continue
            if 'Zrotation' == channel: self.Orientation = glm.rotate(self.Orientation, glm.radians(data[index]), (0.0, 0.0, 1.0)); continue

    def validate(self, raiseExceptions:bool = False) -> bool:
        invalidChannels = self.Channels is None or len(self.Channels) == 0
        if invalidChannels and raiseExceptions:
            raise ValueError(f'Joint "{self.Name}" is missing channel information -> {self.Channels}')
        for child in self.Children:
            if not child.validate(raiseExceptions):
                return False
        return not invalidChannels

    def setOffsetByTransform(self, orientation:glm.quat = glm.quat()):
        self.Position = orientation * self.Position
        orientation = orientation * self.Orientation
        for child in self.Children:
            child.setOffsetByTransform(orientation)

class BVH:
    Hierarchy:Joint
    Motion:numpy.ndarray
    FrameTime:float

    def __init__(self):
        self.Hierarchy = None
        self.Motion = None
        self.FrameTime = None

    @property
    def Frames(self):
        return self.Motion.shape[0] if self.Motion is not None else 0

    def validate(self, raiseExceptions:bool = False) -> bool:
        invalidHierarchy = self.Hierarchy is None or not self.Hierarchy.validate(raiseExceptions)
        if invalidHierarchy and raiseExceptions:
            raise ValueError(f'BVH hierarchy is invalid')
        invalidFrameTime = self.FrameTime is None or self.FrameTime <= 0.0
        if invalidFrameTime and raiseExceptions:
            raise ValueError(f'Frame time must be postive and greater than 0 -> {self.FrameTime}')
        invalidKeyFrames = self.Motion is None or not numpy.issubdtype(self.Motion.dtype, numpy.inexact)
        if invalidKeyFrames and raiseExceptions:
            raise ValueError(f'Motion data is not numeric')
        invalidKeyFrameShape = len(self.Motion.shape) != 2
        if invalidKeyFrameShape and raiseExceptions:
            raise ValueError(f'Motion data is not 2-dimensional -> {self.Motion.shape}')
        invalidKeyFrameSize = self.Motion.shape[1] == len(self.Hierarchy.layout())
        if invalidKeyFrameSize and raiseExceptions:
            raise ValueError(f'Motion data does not match hierarchy size -> {self.Motion.shape[1]} != {len(self.Hierarchy.layout(0))}')
        return not (invalidHierarchy or invalidKeyFrames or invalidKeyFrameShape or invalidKeyFrameSize)

    def readPose(self, frame:int) -> Joint:
        layout = self.Hierarchy.layout()
        for (joint, start, end) in layout:
            joint.deserialize(self.Motion[frame, start:end])
        return self.Hierarchy

    def setAsHierarchy(self, root:Joint) -> None:
        layout = self.Hierarchy.layout(0)
        if layout[-1][-1] != self.Motion.shape[1]:
            raise ValueError(f'Hierarchy channel count does not match motion data length -> {layout[-1][-1]} != {self.Motion.shape[1]}')

        self.Hierarchy = root
        self.Hierarchy.setOffsetByTransform()


