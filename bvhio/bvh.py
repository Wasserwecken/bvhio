import numpy
from .transform import *

class Joint(Transform):
    Name:str
    Channels:list[str]

    def __init__(self, name:str) -> None:
        super().__init__()
        self.Name = name
        self.Channels = []

    def indicies(self) -> list[str]:
        result = [self.Name]
        for child in self.Children:
            result.extend(child.indicies())
        return result

    def index(self, name:str) -> int:
        return self.indicies().index(name)

    def validate(self, raiseExceptions:bool = False) -> bool:
        invalidChannels = self.Channels is None or len(self.Channels) == 0
        if invalidChannels and raiseExceptions:
            raise ValueError(f'Joint "{self.Name}" is missing channel information -> {self.Channels}')
        for child in self.Children:
            if not child.validate(raiseExceptions):
                return False
        return not invalidChannels

    def __repr__(self) -> str:
        return f"{self.Name}"

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
        return len(self.Motion) if self.Motion else 0

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
        invalidKeyFrameSize = self.Motion.shape[1] == len(self.Hierarchy.indicies())
        if invalidKeyFrameSize and raiseExceptions:
            raise ValueError(f'Motion data does not match hierarchy size -> {self.Motion.shape[1]} != {len(self.Hierarchy.indicies())}')
        return not (invalidHierarchy or invalidKeyFrames or invalidKeyFrameShape or invalidKeyFrameSize)
