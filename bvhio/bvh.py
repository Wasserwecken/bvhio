import numpy
from dataclasses import dataclass

@dataclass
class Joint:
    Parent:object = None
    Name:str = None
    Offset:numpy.ndarray = None
    Channels:list[str] = None
    Children:list = None

@dataclass
class BVH:
    Hierarchy:Joint = None
    Motion:numpy.ndarray = None

    @property
    def Frames(self):
        return len(self.Motion) if self.Motion else 0

