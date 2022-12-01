import glm

class Transform:
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
    def SpaceWorld(self) -> glm.mat4:
        return self.Space * (self.Parent.SpaceWorld if self.Parent else glm.mat4())


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
    def Orientation(self, value:glm.vec3) -> None:
        self._Orientation = glm.quat(value)
        self._IsOutdatedLocal = True


    @property
    def Euler(self) -> glm.vec3:
        return glm.eulerAngles(self._Orientation)

    @Euler.setter
    def Euler(self, value:glm.vec3) -> None:
        self._Orientation = glm.quat(value)
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


    def append(self, node:object) -> None:
        if node is self:
            raise ValueError(f'Joint "{self.Name}" cannot be parent of itself')
        if node.Parent is not None:
            node.Parent.remove(node)
        node.Parent = self
        self._Children.append(node)

    def remove(self, node:object) -> bool:
        try:
            self._Children.remove(node)
            node.Parent = None
            node.SpaceParent = glm.mat4()
            return True
        except ValueError:
            return False


    def __init__(self) -> None:
        self._Space = glm.mat4()
        self._SpaceParent = glm.mat4()
        self._Position = glm.vec3()
        self.Scale = glm.vec3(1)
        self.Orientation = glm.quat()

        self._Parent = None
        self._Children = []

    def __repr__(self) -> str:
        return (
            f"Pos: {self._Position:.4f}" +
            f"Scale: {self._Scale:.4f}" +
            f"Forward: {self.ForwardLocal:.4f}"
        )

    def __str__(self) -> str:
        return self.__repr__()
