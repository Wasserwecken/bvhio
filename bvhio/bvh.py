import numpy

class Joint:
    Parent:object
    Name:str
    Offset:numpy.ndarray
    Channels:list[str]
    Children:list

    def __init__(self, name:str) -> None:
        self.Parent = None
        self.Name = name
        self.Offset = None
        self.Channels = []
        self.Children = []

    def append(self, joint:object):
        if joint is self:
            raise ValueError(f'Joint "{self.Name}" cannot be parent of itself')
        if joint.Parent is not None:
            joint.Parent.remove(joint)
        joint.Parent = self
        self.Children.append(joint)

    def remove(self, joint:object) -> bool:
        try:
            self.Children.remove(joint)
            joint.Parent = None
            return True
        except ValueError:
            return False

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
        invalidOffset = self.Offset is None or len(self.Offset) != 3
        if invalidOffset and raiseExceptions:
            raise ValueError(f'Joint "{self.Name}" is missing offset information and must be 3-dimensional -> {self.Offset}')
        for child in self.Children:
            if not child.validate(raiseExceptions):
                return False
        return not (invalidChannels or invalidOffset)

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
