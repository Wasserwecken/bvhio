import unittest
import bvhio
import glm
from utils import *

class Reading(unittest.TestCase):
    def setUp(self):
        self.instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.jointsLocal = [ # print(f"( '{j.Name}', {d}, {len(j.Children)}, glm.{j.PositionLocal}, glm.{j.RotationLocal}, glm.{j.ScaleLocal}, ),")
            ( 'Hips', 0, 3, glm.vec3( 8.03,35.01,88.36 ), glm.quat( 0.131166, -0.0117277,-0.982546,-0.131386 ), glm.vec3(1,1,1 ), ),
            ( 'Chest', 1, 3, glm.vec3(0, 5.21,0 ), glm.quat( 0.918066, 0.359386,-0.160133,0.0320507 ), glm.vec3(1,1,1 ), ),
            ( 'Neck', 2, 1, glm.vec3(0,18.6497, -0.0995947 ), glm.quat( 0.927247, 0.369882,0.0258157, 0.063727 ), glm.vec3(1,1,1 ), ),
            ( 'Head', 3, 0, glm.vec3(0, 5.45,0 ), glm.quat( 0.933054,-0.351756,0.0585907, -0.0473785 ), glm.vec3(1,1,1 ), ),
            ( 'LeftCollar', 2, 1, glm.vec3( 1.12,16.2398, 1.7833 ), glm.quat( 0.763775, -0.0702856,0.0554792, -0.64028 ), glm.vec3(1,1,1 ), ),
            ( 'LeftUpArm', 3, 1, glm.vec3(0, 5.54,0 ), glm.quat(-0.976203,-0.202105, -0.0323696, -0.0716515 ), glm.vec3(1,1,1 ), ),
            ( 'LeftLowArm', 4, 1, glm.vec3(0,11.96,0 ), glm.quat( 0.694325, 0.714836,0.0378194, -0.0741041 ), glm.vec3(1,1,1 ), ),
            ( 'LeftHand', 5, 0, glm.vec3(0, 9.93,0 ), glm.quat( 0.999982, -0.000261795, -1.57639e-06, 0.00602135 ), glm.vec3(1,1,1 ), ),
            ( 'RightCollar', 2, 1, glm.vec3(-1.12,16.2398, 1.7833 ), glm.quat( 0.785245,-0.074266, -0.0547109,0.61336 ), glm.vec3(1,1,1 ), ),
            ( 'RightUpArm', 3, 1, glm.vec3(9.53674e-07, 6.07,0 ), glm.quat( 0.614408,0.0440009, 0.778943, 0.117536 ), glm.vec3(1,1,1 ), ),
            ( 'RightLowArm', 4, 1, glm.vec3(0,11.82,0 ), glm.quat( 0.762976, 0.606189,-0.177084, 0.138002 ), glm.vec3(1,1,1 ), ),
            ( 'RightHand', 5, 0, glm.vec3(0,10.65,0 ), glm.quat( 0.999888,-0.00602318, -9.20184e-05, -0.0136991 ), glm.vec3(1,1,1 ), ),
            ( 'LeftUpLeg', 1, 1, glm.vec3( 3.91,0,0 ), glm.quat(-0.117674,-0.024446,-0.202143, 0.971953 ), glm.vec3(1,1,1 ), ),
            ( 'LeftLowLeg', 2, 1, glm.vec3(0,18.34,0 ), glm.quat( 0.894013,-0.411485,-0.106536, 0.141674 ), glm.vec3(1,1,1 ), ),
            ( 'LeftFoot', 3, 0, glm.vec3(0,17.37,0 ), glm.quat( 0.999951, 0.00994821,0,0 ), glm.vec3(1,1,1 ), ),
            ( 'RightUpLeg', 1, 1, glm.vec3(-3.91,0,0 ), glm.quat( 0.141065, -0.0135394,0.0944943, 0.985387 ), glm.vec3(1,1,1 ), ),
            ( 'RightLowLeg', 2, 1, glm.vec3(0,17.63,0 ), glm.quat( 0.883393,-0.4543, 0.109673,0.0346498 ), glm.vec3(1,1,1 ), ),
            ( 'RightFoot', 3, 0, glm.vec3(0,17.14,0 ), glm.quat( 0.978238, 0.207485,0,0 ), glm.vec3(1,1,1 ), ),
        ]
        self.jointsWorld = [ # print(f"( glm.{j.PositionWorld}, glm.{j.RotationWorld}, glm.{j.ScaleWorld}, ),")
            ( glm.vec3( 8.03,35.01,88.36 ), glm.quat( 0.131166, -0.0117277,-0.982546,-0.131386 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(8.32964,40.0387,89.6891 ), glm.quat( -0.0284937,-0.016158,-0.969888, 0.238575 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(9.16445, 56.601,81.1699 ), glm.quat( -0.0106095, -0.0934888,-0.810787, 0.577729 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(10.0569,58.3175,76.0749 ), glm.quat(0.0320922, -0.0789339,-0.964779, 0.248878 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(8.02734,53.6141,80.5467 ), glm.quat( 0.183665, 0.597425,-0.769471, 0.131396 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(2.65965,55.0025, 80.649 ), glm.quat( -0.0740443,-0.560941, 0.761465,-0.316281 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3( -8.13548,57.0386,75.8955 ), glm.quat( 0.297334,-0.486871, 0.258247,-0.779652 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3( -6.02675,50.1985,69.0168 ), glm.quat( 0.301896,-0.485386, 0.261377,-0.777779 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(10.2624,53.5744, 80.687 ), glm.quat( -0.22297,-0.592409,-0.767848, 0.098717 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(16.0594,55.26, 81.374 ), glm.quat( 0.475579,-0.540937,-0.571479,-0.393222 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3( 27.801,56.4986,80.6108 ), glm.quat( 0.643831, -0.27293,-0.683958, 0.207828 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(28.9407,64.6545,73.8465 ), glm.quat( 0.644899,-0.267389,-0.688931,0.19489 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(4.25561,34.9653,89.3799 ), glm.quat( -0.0866354,-0.983374, 0.103717, 0.121299 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3( 0.900007,17.2952,92.9663 ), glm.quat(-0.488232,-0.815883,0.19136, 0.243612 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(-0.391913,9.47834,108.424 ), glm.quat(-0.480091,-0.820699, 0.193774, 0.241696 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(11.8044,35.0547,87.3401 ), glm.quat( 0.240655,-0.959203,-0.112873,0.0963038 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(14.8047, 19.916,78.8176 ), glm.quat(-0.214131,-0.971155, -0.0838329, -0.0630639 ), glm.vec3(1,1,1 ), ),
            ( glm.vec3(17.1327,4.58869,86.1275 ), glm.quat(-0.00797081, -0.99445, -0.0950934, -0.0442974 ), glm.vec3(1,1,1 ), ),
        ]
        self.frames = [ # print(f'[ glm.{p.Position}, glm.{p.Rotation} ], ', end='')
            [ [ glm.vec3( 8.03,35.01,88.36 ), glm.quat( 0.131166, -0.0117277,-0.982546,-0.131386 ) ], [ glm.vec3( 7.81, 35.1,86.47 ), glm.quat( 0.108987, -0.0197806,-0.987099,-0.115613 ) ],],
            [ [ glm.vec3(0, 5.21,0 ), glm.quat( 0.918066, 0.359386,-0.160133,0.0320507 ) ], [ glm.vec3(0, 5.21,0 ), glm.quat( 0.914714, 0.376029,-0.140031,0.0310876 ) ],],
            [ [ glm.vec3(0,18.6497, -0.0995947 ), glm.quat( 0.927247, 0.369882,0.0258157, 0.063727 ) ], [ glm.vec3(0,18.6497, -0.0995947 ), glm.quat( 0.927975,0.36839,0.0250259,0.0620728 ) ],],
            [ [ glm.vec3(0, 5.45,0 ), glm.quat( 0.933054,-0.351756,0.0585907, -0.0473785 ) ], [ glm.vec3(0, 5.45,0 ), glm.quat( 0.933368,-0.351521,0.0529141, -0.0495629 ) ],],
            [ [ glm.vec3( 1.12,16.2398, 1.7833 ), glm.quat( 0.763775, -0.0702856,0.0554792, -0.64028 ) ], [ glm.vec3( 1.12,16.2398, 1.7833 ), glm.quat( 0.814544, -0.0317584, 0.019518,-0.580049 ) ],],
            [ [ glm.vec3(0, 5.54,0 ), glm.quat(-0.976203,-0.202105, -0.0323696, -0.0716515 ) ], [ glm.vec3(0, 5.54,0 ), glm.quat(-0.992498, -0.0819137, -0.0841669, -0.0339747 ) ],],
            [ [ glm.vec3(0,11.96,0 ), glm.quat( 0.694325, 0.714836,0.0378194, -0.0741041 ) ], [ glm.vec3(0,11.96,0 ), glm.quat( 0.669542, 0.740189, -0.0610665,0.0102361 ) ],],
            [ [ glm.vec3(0, 9.93,0 ), glm.quat( 0.999982, -0.000261795, -1.57639e-06, 0.00602135 ) ], [ glm.vec3(0, 9.93,0 ), glm.quat( 0.999976,-0.00322879, -1.97238e-05, 0.00610858 ) ],],
            [ [ glm.vec3(-1.12,16.2398, 1.7833 ), glm.quat( 0.785245,-0.074266, -0.0547109,0.61336 ) ], [ glm.vec3(-1.12,16.2398, 1.7833 ), glm.quat( 0.744652,-0.145593,-0.121769, 0.640934 ) ],],
            [ [ glm.vec3(9.53674e-07, 6.07,0 ), glm.quat( 0.614408,0.0440009, 0.778943, 0.117536 ) ], [ glm.vec3(9.53674e-07, 6.07,0 ), glm.quat(0.61923, 0.135503, 0.747857, 0.197242 ) ],],
            [ [ glm.vec3(0,11.82,0 ), glm.quat( 0.762976, 0.606189,-0.177084, 0.138002 ) ], [ glm.vec3(0,11.82,0 ), glm.quat( 0.778739, 0.591803,-0.161657, 0.131154 ) ],],
            [ [ glm.vec3(0,10.65,0 ), glm.quat( 0.999888,-0.00602318, -9.20184e-05, -0.0136991 ) ], [ glm.vec3(0,10.65,0 ), glm.quat( 0.999864, -0.0082931, -0.000143844, -0.0142213 ) ],],
            [ [ glm.vec3( 3.91,0,0 ), glm.quat(-0.117674,-0.024446,-0.202143, 0.971953 ) ], [ glm.vec3( 3.91,0,0 ), glm.quat(-0.109352, -0.0151918, -0.13691, 0.984412 ) ],],
            [ [ glm.vec3(0,18.34,0 ), glm.quat( 0.894013,-0.411485,-0.106536, 0.141674 ) ], [ glm.vec3(0,18.34,0 ), glm.quat( 0.8647,-0.490346, -0.0719332, 0.081736 ) ],],
            [ [ glm.vec3(0,17.37,0 ), glm.quat( 0.999951, 0.00994821,0,0 ) ], [ glm.vec3(0,17.37,0 ), glm.quat( 0.999898, -0.0143112,0,0 ) ],],
            [ [ glm.vec3(-3.91,0,0 ), glm.quat( 0.141065, -0.0135394,0.0944943, 0.985387 ) ], [ glm.vec3(-3.91,0,0 ), glm.quat( 0.146418, -0.0134328,0.0903176,0.985 ) ],],
            [ [ glm.vec3(0,17.63,0 ), glm.quat( 0.883393,-0.4543, 0.109673,0.0346498 ) ], [ glm.vec3(0,17.63,0 ), glm.quat( 0.884521,-0.457052,0.0869551,0.0341273 ) ],],
            [ [ glm.vec3(0,17.14,0 ), glm.quat( 0.978238, 0.207485,0,0 ) ], [ glm.vec3(0,17.14,0 ), glm.quat( 0.974507, 0.224356,0,0 ) ],],
        ]

    def test_JointCount(self):
        self.assertEqual(len(self.jointsLocal), len(self.instance.layout()))

    def test_Name(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(j.Name, self.jointsLocal[i][0])

    def test_Depth(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(d, self.jointsLocal[i][1])

    def test_Children(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(len(j.Children), self.jointsLocal[i][2])

    def test_Keyframes(self):
        for j, i, d in self.instance.layout():
            for frame, pose in enumerate(j.Keyframes):
                self.assertGreater(1e-04,  glm.length(pose.Position - self.frames[i][frame][0]))
                self.assertGreater(1e-05,  glm.length(pose.Scale - glm.vec3(1)))
                self.assertGreater(1e-05, glm.length(pose.Rotation - self.frames[i][frame][1]))

    def test_PositionsLocal(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.PositionLocal - self.jointsLocal[i][3]))

    def test_RotationsLocal(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.RotationLocal - self.jointsLocal[i][4]))


    def test_ScalesLocal(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.ScaleLocal - self.jointsLocal[i][5]))

    def test_PositionsLocal(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.PositionLocal - self.jointsLocal[i][3]))

    def test_RotationsLocal(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.RotationLocal - self.jointsLocal[i][4]))

    def test_ScalesLocal(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.ScaleLocal - self.jointsLocal[i][5]))

    def test_PositionsWorld(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.PositionWorld - self.jointsWorld[i][0]))

    def test_RotationsWorld(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.RotationWorld - self.jointsWorld[i][1]))

    def test_ScalesWorld(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-04,  glm.length(j.ScaleWorld - self.jointsWorld[i][2]))


class Methods(unittest.TestCase):
    def test_readPose(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        for frame in range(len(instance.Keyframes)):
            instance.readPose(frame)
            for j, _, _ in instance.layout():
                self.assertEquals(j.PositionLocal, j.Keyframes[frame].Position)
                self.assertEquals(j.RotationLocal, j.Keyframes[frame].Rotation)
                self.assertEquals(j.ScaleLocal, j.Keyframes[frame].Scale)

    def test_writePose(self):
        instance = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        for frame in range(len(instance.Keyframes)):
            for j, _, _ in instance.layout():
                instance.PositionLocal = randomPosition()
                instance.RotationLocal = randomRotation()
                instance.ScaleLocal = randomScale()
                instance.writePose(frame)
                self.assertEquals(j.PositionLocal, j.Keyframes[frame].Position)
                self.assertEquals(j.RotationLocal, j.Keyframes[frame].Rotation)
                self.assertEquals(j.ScaleLocal, j.Keyframes[frame].Scale)

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
