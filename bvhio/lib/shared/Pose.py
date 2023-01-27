import glm


class Pose:
    """Data structure for holding pose data."""

    @property
    def Space(self) -> glm.mat4:
        if self.__isOutdated:
            self._Space = glm.translate(self.Position)
            self._Space = glm.scale(self._Space, self.Scale)
            self._Space = self._Space * glm.mat4_cast(self.Rotation)
            self.__isOutdated = False
        return glm.mat4(self._Space)

    @property
    def Position(self) -> glm.vec3:
        return glm.vec3(self._Position)

    @Position.setter
    def Position(self, value: glm.vec3) -> None:
        self._Position = glm.vec3(value)
        self.__isOutdated = True

    @property
    def Rotation(self) -> glm.quat:
        return glm.quat(self._Rotation)

    @Rotation.setter
    def Rotation(self, value: glm.quat) -> None:
        self._Rotation = glm.quat(value)
        self.__isOutdated = True

    @property
    def Scale(self) -> glm.vec3:
        return glm.vec3(self._Scale)

    @Scale.setter
    def Scale(self, value: glm.vec3) -> None:
        self._Scale = glm.vec3(value)
        self.__isOutdated = True

    def __init__(self, position: glm.vec3 = glm.vec3(), rotation: glm.quat = glm.quat(), scale: glm.vec3 = glm.vec3(1)) -> None:
        self._Position = glm.vec3(position)
        self._Rotation = glm.quat(rotation)
        self._Scale = glm.vec3(scale)
        self.__isOutdated = True

    def __repr__(self) -> str:
        return (f"Pos: {self.Position}, Rot: {self.Rotation}, Scale: {self.Scale}")

    def __str__(self) -> str:
        return self.__repr__()

    def copy(self) -> "Pose":
        return Pose(self.Position, self.Rotation, self.Scale)
