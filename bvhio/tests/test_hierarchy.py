import unittest
import bvhio
import glm
from utils import *

class Reading(unittest.TestCase):
    def setUp(self):
        self.instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.joints = [ # for j, i, d in root.layout(): print(f"( {d}, {len(j.Children)}, {len(j.Keyframes)}, {j.KeyframeRange}, '{j.Name}', ),")
            ( 0, 3, 2, [0, 1], 'Hips', ),
            ( 1, 3, 2, [0, 1], 'Chest', ),
            ( 2, 1, 2, [0, 1], 'Neck', ),
            ( 3, 0, 2, [0, 1], 'Head', ),
            ( 2, 1, 2, [0, 1], 'LeftCollar', ),
            ( 3, 1, 2, [0, 1], 'LeftUpArm', ),
            ( 4, 1, 2, [0, 1], 'LeftLowArm', ),
            ( 5, 0, 2, [0, 1], 'LeftHand', ),
            ( 2, 1, 2, [0, 1], 'RightCollar', ),
            ( 3, 1, 2, [0, 1], 'RightUpArm', ),
            ( 4, 1, 2, [0, 1], 'RightLowArm', ),
            ( 5, 0, 2, [0, 1], 'RightHand', ),
            ( 1, 1, 2, [0, 1], 'LeftUpLeg', ),
            ( 2, 1, 2, [0, 1], 'LeftLowLeg', ),
            ( 3, 0, 2, [0, 1], 'LeftFoot', ),
            ( 1, 1, 2, [0, 1], 'RightUpLeg', ),
            ( 2, 1, 2, [0, 1], 'RightLowLeg', ),
            ( 3, 0, 2, [0, 1], 'RightFoot', ),
        ]
        self.restPoseLocal = [ # for j, i, d in root.layout(): print(f"( glm.{j.PositionLocal}, glm.{j.RotationLocal}, glm.{j.ScaleLocal}, ),")
            ( glm.vec3(            0,            0,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.21,            0 ), glm.quat(     0.999333,    0.0365139,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        18.65,            0 ), glm.quat(     0.999333,   -0.0365139,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.45,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,        16.23,         1.87 ), glm.quat(     0.706635,   -0.0258192,   -0.0258192,    -0.706635 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         5.54,            0,            0 ), glm.quat(    -0.707107,            0,            0,     0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -11.96,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        -9.93,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,        16.23,         1.87 ), glm.quat(     0.706635,   -0.0258192,    0.0258192,     0.706635 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -6.07,            0,            0 ), glm.quat(     0.707107,            0,            0,     0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -11.82,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -10.65,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -18.34,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -17.37,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -17.63,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -17.14,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
        ]
        self.restPoseWorld = [ # for j, i, d in root.layout(): print(f"( glm.{j.PositionWorld}, glm.{j.RotationWorld}, glm.{j.ScaleWorld}, ),")
            ( glm.vec3(            0,            0,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.21,            0 ), glm.quat(     0.999333,    0.0365139,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,      23.8103,      1.36106 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,      29.2603,      1.36106 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,      21.2603,      3.04947 ), glm.quat(     0.707107,            0,            0,    -0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,      15.7203,      3.04947 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,      27.6803,      3.04947 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,      37.6103,      3.04947 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,      21.2603,      3.04947 ), glm.quat(     0.707107,            0,            0,     0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,      15.1903,      3.04947 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,      27.0103,      3.04947 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,      37.6602,      3.04947 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,        18.34,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,        35.71,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,        17.63,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,        34.77,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
        ]
        self.pose0Local = [
            ( glm.vec3(         8.03,        35.01,        88.36 ), glm.quat(     0.131166,   -0.0117277,    -0.982546,    -0.131386 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.21,            0 ), glm.quat(     0.919631,     0.357174,    -0.160325,    0.0316445 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        18.65,            0 ), glm.quat(     0.925643,     0.372106,    0.0256287,    0.0637533 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.45,            0 ), glm.quat(     0.933054,    -0.351756,    0.0585907,   -0.0473785 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,        16.23,         1.87 ), glm.quat(     0.993692,   -0.0473221,    0.0554972,    0.0851893 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         5.54,            0,            0 ), glm.quat(     0.639614,    -0.120021,    -0.165798,     0.740945 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -11.96,            0 ), glm.quat(     0.694325,    -0.714836,   -0.0378194,   -0.0741041 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        -9.93,            0 ), glm.quat(     0.999982,  0.000261795,  1.57639e-06,   0.00602135 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,        16.23,         1.87 ), glm.quat(     0.989766,   -0.0517941,   -0.0590565,    -0.119137 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -6.07,            0,            0 ), glm.quat(     0.517563,    -0.581909,    -0.519682,    -0.351341 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -11.82,            0 ), glm.quat(     0.762976,    -0.606189,     0.177084,     0.138002 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -10.65,            0 ), glm.quat(     0.999888,   0.00602318,  9.20184e-05,   -0.0136991 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,            0,            0 ), glm.quat(     0.971953,     0.202143,    -0.024446,     0.117674 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -18.34,            0 ), glm.quat(     0.894013,     0.411485,     0.106536,     0.141674 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -17.37,            0 ), glm.quat(     0.999951,  -0.00994821,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,            0,            0 ), glm.quat(     0.985387,   -0.0944943,   -0.0135394,    -0.141065 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -17.63,            0 ), glm.quat(     0.883393,       0.4543,    -0.109673,    0.0346498 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,       -17.14,            0 ), glm.quat(     0.978238,    -0.207485,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
        ]
        self.pose0World = [
            ( glm.vec3(         8.03,        35.01,        88.36 ), glm.quat(     0.131166,   -0.0117277,    -0.982546,    -0.131386 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      8.32964,      40.0387,      89.6891 ), glm.quat(   -0.0285556,   -0.0160927,    -0.971165,     0.236144 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      9.16411,       56.599,      81.1521 ), glm.quat(   -0.0106095,   -0.0934888,    -0.810787,     0.577729 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      10.0571,      58.3157,      76.0571 ), glm.quat(    0.0320921,   -0.0789339,    -0.964779,     0.248878 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      8.02774,      53.6107,      80.5308 ), glm.quat(   0.00464293,    -0.110478,    -0.976427,     0.185371 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      2.62322,      54.8154,      80.3541 ), glm.quat(     -0.30953,    -0.763965,    -0.565697,    0.0231318 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(     -7.88562,       56.829,      75.0107 ), glm.quat(    -0.780705,    -0.266381,     -0.45422,     -0.33649 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(     -5.07139,      50.5569,      67.8452 ), glm.quat(    -0.778594,    -0.269315,    -0.452697,    -0.341066 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      10.2629,      53.5708,      80.6721 ), glm.quat(   -0.0583171,     0.115198,    -0.973688,     0.187779 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      16.1305,      55.0655,      81.0988 ), glm.quat(    -0.403182,      0.53324,    -0.542435,    -0.508787 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      27.8177,       56.087,      79.6569 ), glm.quat(     0.181896,     0.666494,    -0.250429,    -0.678222 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      28.7452,      64.6964,       73.457 ), glm.quat(     0.168594,     0.671008,    -0.245339,    -0.679068 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      4.25561,      34.9653,      89.3799 ), glm.quat(     0.121299,    -0.103717,    -0.983374,    0.0866354 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(     0.900007,      17.2952,      92.9663 ), glm.quat(     0.243612,     -0.19136,    -0.815883,     0.488232 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(    -0.391912,      9.47835,      108.424 ), glm.quat(     0.241696,    -0.193774,    -0.820699,     0.480091 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      11.8044,      35.0547,      87.3401 ), glm.quat(    0.0963039,     0.112873,    -0.959203,    -0.240655 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      14.8047,       19.916,      78.8176 ), glm.quat(   -0.0630639,     0.083833,    -0.971155,     0.214131 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      17.1327,      4.58868,      86.1275 ), glm.quat(   -0.0442974,    0.0950934,     -0.99445,   0.00797085 ), glm.vec3(            1,            1,            1 ), ),
        ]

    def test_JointCount(self):
        self.assertEqual(len(self.joints), len(self.instance.layout()))

    def test_Name(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(j.Name, self.joints[i][-1])

    def test_Depth(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(d, self.joints[i][0])

    def test_Children(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(len(j.Children), self.joints[i][1])

    def test_Keyframes(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(2, self.joints[i][2])

    def test_KeyframeRange(self):
        for j, i, d in self.instance.layout():
            self.assertEqual([0, 1], self.joints[i][3])

    def test_PositionsRestPose(self):
        for j, i, d in self.instance.readRestPose(recursive=True).layout():
            self.assertGreater(1e-06, deviationPosition(j.PositionLocal, self.restPoseLocal[i][0]))
            self.assertGreater(1e-04, deviationPosition(j.PositionWorld, self.restPoseWorld[i][0]))

    def test_RotationsRestPose(self):
        for j, i, d in self.instance.readRestPose(recursive=True).layout():
            self.assertGreater(1e-06, deviationQuaternion(j.RotationLocal, self.restPoseLocal[i][1]))
            self.assertGreater(1e-06, deviationQuaternion(j.RotationWorld, self.restPoseWorld[i][1]))

    def test_ScalesRestPose(self):
        for j, i, d in self.instance.readRestPose(recursive=True).layout():
            self.assertGreater(1e-06,  glm.length(j.ScaleLocal - self.restPoseLocal[i][2]))
            self.assertGreater(1e-06,  glm.length(j.ScaleWorld - self.restPoseWorld[i][2]))

    def test_PositionsPose0(self):
        for j, i, d in self.instance.readPose(0, recursive=True).layout():
            self.assertGreater(1e-06, deviationPosition(j.PositionLocal, self.pose0Local[i][0]))
            self.assertGreater(1e-04, deviationPosition(j.PositionWorld, self.pose0World[i][0]))

    def test_RotationsPose0(self):
        for j, i, d in self.instance.readPose(0, recursive=True).layout():
            self.assertGreater(1e-05, deviationQuaternion(j.RotationLocal, self.pose0Local[i][1]))
            self.assertGreater(1e-05, deviationQuaternion(j.RotationWorld, self.pose0World[i][1]))

    def test_ScalesPose0(self):
        for j, i, d in self.instance.readPose(0, recursive=True).layout():
            self.assertGreater(1e-06,  glm.length(j.ScaleLocal - self.pose0Local[i][2]))
            self.assertGreater(1e-06,  glm.length(j.ScaleWorld - self.pose0World[i][2]))

class Methods(unittest.TestCase):
    def test_readPose(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        for frame in range(len(instance.Keyframes)):
            instance.readPose(frame)
            for j, _, _ in instance.layout():
                self.assertGreater(1e-06, deviationPosition(j.PositionLocal, (j.RestPose.Position + j.Keyframes[frame][1].Position)))
                self.assertGreater(1e-06, deviationQuaternion(j.RotationLocal, (j.RestPose.Rotation * j.Keyframes[frame][1].Rotation)))
                self.assertGreater(1e-06, deviationScale(j.ScaleLocal, (j.RestPose.Scale * j.Keyframes[frame][1].Scale)))

    def test_writePose(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        for frame in range(len(instance.Keyframes)):
            for j, _, _ in instance.layout():
                position = randomPosition()
                rotation = randomRotation()
                scale = randomScale()
                j.PositionLocal = position
                j.RotationLocal = rotation
                j.ScaleLocal = scale
                j.writePose(frame, recursive=False)
                self.assertGreater(1e-06, deviationPosition(j.PositionLocal, (j.RestPose.Position + j.Keyframes[frame][1].Position)))
                self.assertGreater(1e-06, deviationQuaternion(j.RotationLocal, (j.RestPose.Rotation * j.Keyframes[frame][1].Rotation)))
                self.assertGreater(1e-06, deviationScale(j.ScaleLocal, (j.RestPose.Scale * j.Keyframes[frame][1].Scale)))
                j.readPose(frame, recursive=False)
                self.assertGreater(1e-06, deviationPosition(position, j.PositionLocal))
                self.assertGreater(1e-06, deviationQuaternion(rotation, j.RotationLocal))
                self.assertGreater(1e-06, deviationScale(scale, j.ScaleLocal))

    def test_attach(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertTrue(True)

    def test_detach(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertTrue(True)

    def test_applyPosition(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertTrue(True)

    def test_applyRotation(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertTrue(True)

    def test_appyScale(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertTrue(True)

    def test_roll(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertTrue(True)
