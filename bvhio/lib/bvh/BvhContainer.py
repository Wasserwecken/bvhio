from .RootPose import RootPose


class BvhContainer:
    """Container for the information of the bvh file.

    Root is the recursive definition of the skeleton.

    Frame time the frame time.

    Frams are the count of keyframes of the motion."""
    Root: RootPose
    FrameTime: float
    FrameCount: int

    def __init__(self):
        self.Root: RootPose = None
        self.FrameTime: float = None
        self.FrameCount: int = None
