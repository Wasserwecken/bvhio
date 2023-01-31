from .BvhJoint import BvhJoint


class BvhContainer:
    """Container for the information of the bvh file.

    Root is the recursive definition of the skeleton.

    Frame time the frame time.

    Frams are the count of keyframes of the motion."""
    Root: BvhJoint
    FrameCount: int
    FrameTime: float

    def __init__(self, root: BvhJoint = None, frameCount: int = None, frameTime: float = None):
        self.Root: BvhJoint = root
        self.FrameCount: int = frameCount
        self.FrameTime: float = frameTime
