import glm
from ..shared import Pose


class RootPose:
    """Data structure for the bvh skeleton definition. Contains the attributes as in the BVH file.

    Keyframes contain the motion data."""
    Name: str
    Offset: glm.vec3
    EndSite: glm.vec3
    Keyframes: list[Pose]
    Channels: list[str]
    Children: list["RootPose"]

    def __init__(self, name: str, offset: glm.vec3 = glm.vec3()) -> None:
        self.Name = name
        self.Offset = offset
        self.EndSite = glm.vec3(0, 1, 0)
        self.Keyframes = []
        self.Channels = []
        self.Children = []

    def __repr__(self) -> str:
        return (f"{self.Name}")

    def __str__(self) -> str:
        return self.__repr__()

    def getTip(self) -> glm.vec3:
        """Calculates the tip of the defined bone.

        The tip position is the average position of all children in local space without rotation.
        If there is no child joint, the EndSite value will be returned."""
        children = len(self.Children)
        if children == 1: return self.Children[0].Offset
        elif children > 1: return sum(child.Offset for child in self.Children) / children
        else: return self.EndSite if glm.length(self.EndSite) > 0.001 else glm.vec3(0, 1, 0)

    def getLength(self) -> float:
        """Length of the bone which is based on the tip."""
        return glm.length(self.getTip())

    def getRotation(self) -> glm.quat:
        """calculate the bone rotation based on the tip."""
        # https://arrowinmyknee.com/2021/02/10/how-to-get-rotation-from-two-vectors/
        dir = glm.normalize(self.getTip())
        axis = glm.vec3(0, 1, 0)
        dot = glm.dot(axis, dir)

        if dot < -0.999: return glm.quat(0, 0, 0, 1)
        return glm.angleAxis(glm.acos(dot), glm.cross(axis, dir))

    def layout(self, index: int = 0, depth: int = 0) -> list[tuple["RootPose", int, int]]:
        """Returns the hierarchical layout of this joint and its children recursivly."""
        result = [[self, index, depth]]
        for child in self.Children:
            result.extend(child.layout(result[-1][1] + 1, depth + 1))
        return result
