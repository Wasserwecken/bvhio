import glm
import transform as tr

class Transform:
    @property
    def Name(self) -> str:
        return self._Name
    @Name.setter
    def Name(self, value:str) -> None:
        self._Name = value

    @property
    def IsOutdatedLocal(self) -> bool:
        return self._IsOutdatedLocal

    @property
    def Space(self) -> glm.mat4:
        if self._IsOutdatedLocal:
            self._Space = glm.translate(self._Position)
            self._Space = glm.scale(self._Space, self._Scale)
            self._Space = glm.mat4_cast(self._Orientation) * self._Space
            self._IsOutdatedLocal = False
        return self._Space
    @Space.setter
    def Space(self, value:glm.mat4) -> None:
        self._Space = value
        glm.decompose(value,
            self._Scale,
            self._Orientation,
            self._Position,
            glm.vec3(),
            glm.vec4())
        self._IsOutdatedLocal = False

    @property
    def SpaceParent(self) -> glm.mat4:
        return (self.Parent.SpaceWorld if self.Parent else glm.mat4())

    @property
    def SpaceWorld(self) -> glm.mat4:
        return self.Space * self.SpaceParent

    @property
    def Position(self) -> glm.vec3:
        return self._Position
    @Position.setter
    def Position(self, value:glm.vec3) -> None:
        self._Position = value
        self._IsOutdatedLocal = True

    @property
    def Scale(self) -> glm.vec3:
        return self._Scale
    @Scale.setter
    def Scale(self, value:glm.vec3) -> None:
        self._Scale = value
        self._IsOutdatedLocal = True

    @property
    def Orientation(self) -> glm.quat:
        return self._Orientation
    @Orientation.setter
    def Orientation(self, value:glm.quat) -> None:
        self._Orientation = value
        self._IsOutdatedLocal = True

    @property
    def Forward(self) -> glm.vec3:
        return self._Orientation * glm.vec3(0, 0, 1)

    @property
    def Right(self) -> glm.vec3:
        return self._Orientation * glm.vec3(1, 0, 0)

    @property
    def Up(self) -> glm.vec3:
        return self._Orientation * glm.vec3(0, 1, 0)

    @property
    def Parent(self) -> object:
        return self._Parent
    @Parent.setter
    def Parent(self, value:object) -> None:
        self._Parent = value

    @property
    def Children(self) -> list[object]:
        return self._Children

    def __init__(self) -> None:
        self._Space = glm.mat4()
        self._Position = glm.vec3()
        self.Scale = glm.vec3(1)
        self.Orientation = glm.quat()

        self._Parent = None
        self._Children = []

    def __repr__(self) -> str:
        return (f"Name: {self._Name}")

    def __str__(self) -> str:
        return (f"Name: {self._Name}"
            + f"\nPos: {self._Position}"
            + f"\nRot: {self.Euler}"
            + f"\nScale: {self._Scale}"
            + f"\nChildren: {len(self._Children)}"
        )

    def GetEuler(self, order:str = 'ZXY') -> glm.vec3:
        return glm.degrees(glm.vec3(tr.euler.to(glm.transpose(glm.mat3_cast(self.Orientation)), order)))


    def append(self, node:object) -> None:
        if node is self:
            raise ValueError(f'Joint "{self.Name}" cannot be parent of itself')
        if node.Parent is not None:
            node.Parent.remove(node)
        node.Parent = self
        self._Children.append(node)

    # def remove(self, node:object) -> bool:
    #     try:
    #         self._Children.remove(node)
    #         node.Parent = None
    #         return True
    #     except ValueError:
    #         return False

    # def clearChildren(self) -> None:
    #     for child in self.Children:
    #         child.Parent = None
    #     self._Children.clear()

    def applyRotation(self, recursive:bool = False):
        for child in self.Children:
            child.Position = self.Orientation * child.Position
            child.Orientation = self.Orientation * child.Orientation
            if recursive: child.applyRotation(recursive)
        self.Orientation = glm.quat()
