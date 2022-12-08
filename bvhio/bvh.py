import numpy
import glm
import transform as tr

class Joint(tr.Transform):
    Origin:tuple[glm.vec3, glm.quat]
    Motion:list[tuple[glm.vec3, glm.quat]]
    Channels:list[str]

    def __init__(self, name:str) -> None:
        super().__init__()
        self.Name = name
        self.Channels = []
        self.Motion = []
        self.Origin = [glm.vec3(), glm.quat()]

    def layout(self, startIndex:int = 0) -> list[object, int, int]:
        endIndex = startIndex+len(self.Channels)
        result = [[self, startIndex, endIndex]]

        for child in self.Children:
            result.extend(child.layout(result[-1][2]))
        return result

    def serializeMotion(self) -> numpy.ndarray:
        result:list[list[float]] = []
        for (position, orientation) in self.Motion:
            resultData:list[float] = []
            rotOrder = ''.join([rot[0] for rot in self.Channels if rot[1:] == 'rotation'])
            rotMat = glm.transpose(glm.mat3_cast(orientation))
            rotation = glm.degrees(glm.vec3(tr.euler.fromMatTo(rotMat, rotOrder)))
            for channel in self.Channels:
                if 'Xposition' == channel: resultData.append(position.x); continue
                if 'Yposition' == channel: resultData.append(position.y); continue
                if 'Zposition' == channel: resultData.append(position.z); continue
                if 'Xrotation' == channel: resultData.append(rotation.x); continue
                if 'Yrotation' == channel: resultData.append(rotation.y); continue
                if 'Zrotation' == channel: resultData.append(rotation.z); continue
            result.append(resultData)
        return numpy.array(result)

    def deserializeMotion(self, data:numpy.ndarray) -> None:
        self.Motion.clear()
        for frame in data:
            position = glm.vec3()
            orientation = glm.quat()
            for (index, channel) in enumerate(self.Channels):
                if 'Xposition' == channel: position.x = frame[index]; continue
                if 'Yposition' == channel: position.y = frame[index]; continue
                if 'Zposition' == channel: position.z = frame[index]; continue
                if 'Xrotation' == channel: orientation = glm.rotate(orientation, glm.radians(frame[index]), (1.0, 0.0, 0.0)); continue
                if 'Yrotation' == channel: orientation = glm.rotate(orientation, glm.radians(frame[index]), (0.0, 1.0, 0.0)); continue
                if 'Zrotation' == channel: orientation = glm.rotate(orientation, glm.radians(frame[index]), (0.0, 0.0, 1.0)); continue
            self.Motion.append([position, orientation])

    def readOrigin(self) -> None:
        self.Position = self.Origin[0]
        self.Orientation = self.Origin[1]
        for child in self.Children:
            child.readOrigin()

    def writeOrigin(self) -> None:
        self.Origin[0] = self.Position
        self.Origin[1] = self.Orientation
        for child in self.Children:
            child.writeOrigin()

    def readPose(self, frame:int) -> None:
        self.Position = self.Motion[frame][0]
        self.Orientation = self.Motion[frame][1]
        for child in self.Children:
            child.readPose(frame)

    def writePose(self, frame:int) -> None:
        self.Motion[frame][0] = self.Position
        self.Motion[frame][1] = self.Orientation
        for child in self.Children:
            child.writePose(frame)

    def applyRotation(self, recursive: bool = False):
        # for child in self.Children:
        #     for frame in range(0, len(child.Motion)):
        #         child.Motion[frame][0] = self.Orientation * child.Motion[frame][0]
        #         child.Motion[frame][1] = self.Orientation * child.Motion[frame][1]
        return super().applyRotation(recursive)

class BVH:
    Hierarchy:Joint
    FrameTime:float

    def __init__(self):
        self.Hierarchy = None
        self.FrameTime = None

    @property
    def Frames(self) -> float:
        return self.Motion.shape[0] if self.Motion is not None else 0

    @property
    def Motion(self) -> numpy.ndarray:
        layout = self.Hierarchy.layout(0)
        result = layout[0][0].serializeMotion()
        for i in range(1, len(layout)):
            result = numpy.append(result, layout[i][0].serializeMotion(), 1)
        return result
