import glm


class Pose:
    """Data structure for holding pose data."""

    @property
    def Position(self) -> glm.vec3: return glm.vec3(self._Position)
    @Position.setter
    def Position(self, value: glm.vec3) -> None: self._Position = glm.vec3(value)

    @property
    def Rotation(self) -> glm.quat: return glm.quat(self._Rotation)
    @Rotation.setter
    def Rotation(self, value: glm.quat) -> None: self._Rotation = glm.quat(value)

    @property
    def Scale(self) -> glm.vec3: return glm.vec3(self._Scale)
    @Scale.setter
    def Scale(self, value: glm.vec3) -> None: self._Scale = glm.vec3(value)

    def __init__(self, position: glm.vec3 = glm.vec3(), rotation: glm.quat = glm.quat(), scale: glm.vec3 = glm.vec3(1)) -> None:
        self._Position = glm.vec3(position)
        self._Rotation = glm.quat(rotation)
        self._Scale = glm.vec3(scale)

    def __repr__(self) -> str:
        return (f"Pos: {self.Position}, Rot: {self.Rotation}, Scale: {self.Scale}")

    def __str__(self) -> str:
        return self.__repr__()
