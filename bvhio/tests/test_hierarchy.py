import unittest
import bvhio
import glm
from utils import *

class Reading(unittest.TestCase):
    def setUp(self):
        self.instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.joints = [ # for j, i, d in root.layout(): print(f"( {d}, {len(j.Children)}, {len(j.Keyframes)}, {j.KeyframeRange}, '{j.Name}', ),")
            ( 0, 3, 2, (0, 1), 'Hips', ),
            ( 1, 3, 2, (0, 1), 'Chest', ),
            ( 2, 1, 2, (0, 1), 'Neck', ),
            ( 3, 0, 2, (0, 1), 'Head', ),
            ( 2, 1, 2, (0, 1), 'LeftCollar', ),
            ( 3, 1, 2, (0, 1), 'LeftUpArm', ),
            ( 4, 1, 2, (0, 1), 'LeftLowArm', ),
            ( 5, 0, 2, (0, 1), 'LeftHand', ),
            ( 2, 1, 2, (0, 1), 'RightCollar', ),
            ( 3, 1, 2, (0, 1), 'RightUpArm', ),
            ( 4, 1, 2, (0, 1), 'RightLowArm', ),
            ( 5, 0, 2, (0, 1), 'RightHand', ),
            ( 1, 1, 2, (0, 1), 'LeftUpLeg', ),
            ( 2, 1, 2, (0, 1), 'LeftLowLeg', ),
            ( 3, 0, 2, (0, 1), 'LeftFoot', ),
            ( 1, 1, 2, (0, 1), 'RightUpLeg', ),
            ( 2, 1, 2, (0, 1), 'RightLowLeg', ),
            ( 3, 0, 2, (0, 1), 'RightFoot', ),
        ]
        self.restPoseLocal = [ # for j, i, d in root.layout(): print(f"( glm.{j.Position}, glm.{j.Rotation}, glm.{j.Scale}, ),")
            ( glm.vec3(            0,            0,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.21,            0 ), glm.quat(     0.999333,    0.0365139,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,      18.6003,     -1.36106 ), glm.quat(     0.999333,   -0.0365139,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.45,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,      16.3232,     0.680562 ), glm.quat(     0.706635,   -0.0258192,   -0.0258192,    -0.706635 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3( -4.76837e-07,         5.54,            0 ), glm.quat(    -0.707107,            0,            0,     0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        11.96,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         9.93,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,      16.3232,     0.680562 ), glm.quat(     0.706635,   -0.0258192,    0.0258192,     0.706635 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(  9.53674e-07,         6.07,            0 ), glm.quat(     0.707107,            0,            0,     0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        11.82,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        10.65,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        18.34,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        17.37,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        17.63,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        17.14,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
        ]
        self.restPoseWorld = [ # for j, i, d in root.layout(): print(f"( glm.{j.PositionWorld}, glm.{j.RotationWorld}, glm.{j.ScaleWorld}, ),")
            ( glm.vec3(            0,            0,            0 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.21,            0 ), glm.quat(     0.999333,    0.0365139,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        23.86,  1.19209e-07 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        29.31,  1.19209e-07 ), glm.quat(            1,            0,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,        21.44,         1.87 ), glm.quat(     0.707107,            0,            0,    -0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         6.66,        21.44,         1.87 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         6.66,         9.48,         1.87 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         6.66,    -0.450002,         1.87 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,        21.44,         1.87 ), glm.quat(     0.707107,            0,            0,     0.707107 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -7.19,        21.44,         1.87 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -7.19,         9.62,         1.87 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -7.19,        -1.03,         1.87 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,       -18.34,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,       -35.71,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,            0,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,       -17.63,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,       -34.77,            0 ), glm.quat(            0,            0,            0,            1 ), glm.vec3(            1,            1,            1 ), ),
        ]
        self.pose0Local = [
            ( glm.vec3(         8.03,        35.01,        88.36 ), glm.quat(     0.131166,   -0.0117277,    -0.982546,    -0.131386 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.21,            0 ), glm.quat(     0.905976,     0.390515,    -0.159062,    0.0374775 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,      18.6003,     -1.36106 ), glm.quat(     0.938613,     0.338059,    0.0279395,     0.062775 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         5.45,            0 ), glm.quat(     0.933054,    -0.351756,    0.0585907,   -0.0473785 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         1.12,      16.3232,     0.680562 ), glm.quat(     0.760453,   -0.0960347,    0.0337522,    -0.641365 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3( -4.76837e-07,         5.54,            0 ), glm.quat(    -0.976203,    -0.202105,   -0.0323696,   -0.0716515 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        11.96,            0 ), glm.quat(     0.694325,     0.714836,    0.0378194,   -0.0741041 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,         9.93,            0 ), glm.quat(     0.999982, -0.000261795, -1.57639e-06,   0.00602135 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -1.12,      16.3232,     0.680562 ), glm.quat(     0.781762,    -0.100736,   -0.0338954,     0.614452 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(  9.53674e-07,         6.07,            0 ), glm.quat(     0.614408,    0.0440009,     0.778943,     0.117536 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        11.82,            0 ), glm.quat(     0.762976,     0.606189,    -0.177084,     0.138002 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        10.65,            0 ), glm.quat(     0.999888,  -0.00602318, -9.20184e-05,   -0.0136991 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(         3.91,            0,            0 ), glm.quat(    -0.117674,    -0.024446,    -0.202143,     0.971953 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        18.34,            0 ), glm.quat(     0.894013,    -0.411485,    -0.106536,     0.141674 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        17.37,            0 ), glm.quat(     0.999951,   0.00994821,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(        -3.91,            0,            0 ), glm.quat(     0.141065,   -0.0135394,    0.0944943,     0.985387 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        17.63,            0 ), glm.quat(     0.883393,      -0.4543,     0.109673,    0.0346498 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(            0,        17.14,            0 ), glm.quat(     0.978238,     0.207485,            0,            0 ), glm.vec3(            1,            1,            1 ), ),
        ]
        self.pose0World = [
            ( glm.vec3(         8.03,        35.01,        88.36 ), glm.quat(     0.131166,   -0.0117277,    -0.982546,    -0.131386 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      8.32964,      40.0387,      89.6891 ), glm.quat(    -0.027949,   -0.0171246,    -0.961895,     0.271448 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      9.16411,       56.599,      81.1521 ), glm.quat(   -0.0106095,   -0.0934888,    -0.810788,     0.577729 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      10.0571,      58.3157,      76.0571 ), glm.quat(    0.0320922,   -0.0789339,    -0.964779,     0.248878 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      8.02774,      53.6106,      80.5308 ), glm.quat(     0.183665,     0.597426,    -0.769471,     0.131396 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      2.66686,      55.0047,      80.6263 ), glm.quat(   -0.0740443,    -0.560941,     0.761465,    -0.316281 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(     -8.11043,      57.0454,       75.859 ), glm.quat(     0.297335,    -0.486871,     0.258247,    -0.779652 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(     -6.00359,      50.1956,      68.9853 ), glm.quat(     0.301897,    -0.485386,     0.261377,    -0.777779 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      10.2629,      53.5708,      80.6721 ), glm.quat(     -0.22297,     -0.59241,    -0.767848,     0.098717 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      16.0524,       55.262,      81.3554 ), glm.quat(     0.475579,    -0.540937,     -0.57148,    -0.393222 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      27.7812,      56.5094,      80.5862 ), glm.quat(     0.643831,     -0.27293,    -0.683958,     0.207828 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      28.9073,      64.6527,      73.8156 ), glm.quat(     0.644899,    -0.267389,    -0.688931,      0.19489 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      4.25561,      34.9653,      89.3799 ), glm.quat(   -0.0866354,    -0.983374,     0.103717,     0.121299 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(     0.900007,      17.2952,      92.9663 ), glm.quat(    -0.488232,    -0.815883,      0.19136,     0.243612 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(    -0.391913,      9.47834,      108.424 ), glm.quat(    -0.480091,    -0.820699,     0.193774,     0.241696 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      11.8044,      35.0547,      87.3401 ), glm.quat(     0.240655,    -0.959203,    -0.112873,    0.0963038 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      14.8047,       19.916,      78.8176 ), glm.quat(    -0.214131,    -0.971155,   -0.0838329,   -0.0630639 ), glm.vec3(            1,            1,            1 ), ),
            ( glm.vec3(      17.1327,      4.58869,      86.1275 ), glm.quat(  -0.00797081,     -0.99445,   -0.0950934,   -0.0442974 ), glm.vec3(            1,            1,            1 ), ),
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
            self.assertEqual(j.getKeyframeRange(includeChildren=True), self.joints[i][3])

    def test_PositionsRestPose(self):
        for j, i, d in self.instance.loadRestPose(recursive=True).layout():
            self.assertGreater(1e-04, deviationPosition(j.Position, self.restPoseLocal[i][0]))
            self.assertGreater(1e-04, deviationPosition(j.PositionWorld, self.restPoseWorld[i][0]))

    def test_RotationsRestPose(self):
        for j, i, d in self.instance.loadRestPose(recursive=True).layout():
            self.assertGreater(1e-06, deviationQuaternion(j.Rotation, self.restPoseLocal[i][1]))
            self.assertGreater(1e-06, deviationQuaternion(j.RotationWorld, self.restPoseWorld[i][1]))

    def test_ScalesRestPose(self):
        for j, i, d in self.instance.loadRestPose(recursive=True).layout():
            self.assertGreater(1e-06,  glm.length(j.Scale - self.restPoseLocal[i][2]))
            self.assertGreater(1e-06,  glm.length(j.ScaleWorld - self.restPoseWorld[i][2]))

    def test_PositionsPose0(self):
        for j, i, d in self.instance.loadPose(0, recursive=True).layout():
            self.assertGreater(1e-04, deviationPosition(j.Position, self.pose0Local[i][0]))
            self.assertGreater(1e-03, deviationPosition(j.PositionWorld, self.pose0World[i][0]))

    def test_RotationsPose0(self):
        for j, i, d in self.instance.loadPose(0, recursive=True).layout():
            self.assertGreater(1e-05, deviationQuaternion(j.Rotation, self.pose0Local[i][1]))
            self.assertGreater(1e-05, deviationQuaternion(j.RotationWorld, self.pose0World[i][1]))

    def test_ScalesPose0(self):
        for j, i, d in self.instance.loadPose(0, recursive=True).layout():
            self.assertGreater(1e-06,  glm.length(j.Scale - self.pose0Local[i][2]))
            self.assertGreater(1e-06,  glm.length(j.ScaleWorld - self.pose0World[i][2]))

class Methods(unittest.TestCase):
    def test_write_read_RestPose(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        instance.loadRestPose(recursive=True)
        restPose = [(joint.PositionWorld, joint.RotationWorld, joint.ScaleWorld) for joint, _ , _ in instance.layout()]
        instance.loadPose(0, recursive=True)
        animPose = [(joint.PositionWorld, joint.RotationWorld, joint.ScaleWorld) for joint, _ , _ in instance.layout()]

        instance.loadRestPose(recursive=True)
        instance.writeRestPose(recursive=True, keep=None)
        instance.loadRestPose(recursive=True)
        for j, i, d in instance.layout():
            self.assertGreater(1e-04, deviationPosition(restPose[i][0], j.PositionWorld))
            self.assertGreater(1e-04, deviationQuaternion(restPose[i][1], j.RotationWorld))
            self.assertGreater(1e-04, deviationScale(restPose[i][2], j.ScaleWorld))
        instance.loadPose(0, recursive=True)
        for j, i, d in instance.layout():
            self.assertGreater(1e-04, deviationPosition(animPose[i][0], j.PositionWorld))
            self.assertGreater(1e-04, deviationQuaternion(animPose[i][1], j.RotationWorld))
            self.assertGreater(1e-04, deviationScale(animPose[i][2], j.ScaleWorld))

        instance.loadRestPose(recursive=True)
        instance.writeRestPose(recursive=True, keep=['position', 'rotation', 'scale'])
        instance.loadRestPose(recursive=True)
        for j, i, d in instance.layout():
            self.assertGreater(1e-04, deviationPosition(restPose[i][0], j.PositionWorld))
            self.assertGreater(1e-04, deviationQuaternion(restPose[i][1], j.RotationWorld))
            self.assertGreater(1e-04, deviationScale(restPose[i][2], j.ScaleWorld))
        instance.loadPose(0, recursive=True)
        for j, i, d in instance.layout():
            self.assertGreater(1e-04, deviationPosition(animPose[i][0], j.PositionWorld))
            self.assertGreater(1e-04, deviationQuaternion(animPose[i][1], j.RotationWorld))
            self.assertGreater(1e-04, deviationScale(animPose[i][2], j.ScaleWorld))

    def test_write_read_Pose(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        instance.loadRestPose(recursive=True)
        restPose = [(joint.PositionWorld, joint.RotationWorld, joint.ScaleWorld) for joint, _ , _ in instance.layout()]

        for frame in range(len(instance.Keyframes)):
            instance.loadPose(frame, recursive=True)
            pose = [(joint.PositionWorld, joint.RotationWorld, joint.ScaleWorld) for joint, _ , _ in instance.layout()]

            instance.writePose(frame, recursive=True)
            instance.loadPose(frame, recursive=True)
            for j, i, d in instance.layout():
                self.assertGreater(1e-04, deviationPosition(pose[i][0], j.PositionWorld))
                self.assertGreater(1e-04, deviationQuaternion(pose[i][1], j.RotationWorld))
                self.assertGreater(1e-04, deviationScale(pose[i][2], j.ScaleWorld))
            instance.loadRestPose(recursive=True)
            for j, i, d in instance.layout():
                self.assertGreater(1e-04, deviationPosition(restPose[i][0], j.PositionWorld))
                self.assertGreater(1e-04, deviationQuaternion(restPose[i][1], j.RotationWorld))
                self.assertGreater(1e-04, deviationScale(restPose[i][2], j.ScaleWorld))

    def test_roll(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        instance.loadRestPose(recursive=True)
        childPose = [(joint.PositionWorld, joint.RotationWorld, joint.ScaleWorld) for joint in instance.Children]

        for step in range(72):
            instance.roll(step*5, recursive=False)
            for i, child in enumerate(instance.Children):
                self.assertGreater(1e-04, deviationPosition(childPose[i][0], child.PositionWorld))
                self.assertGreater(1e-04, deviationQuaternion(childPose[i][1], child.RotationWorld))
                self.assertGreater(1e-04, deviationScale(childPose[i][2], child.ScaleWorld))

        self.assertTrue(True)
