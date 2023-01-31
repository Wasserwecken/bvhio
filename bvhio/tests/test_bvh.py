import unittest
import bvhio
import glm
from utils import *

class Container(unittest.TestCase):
    def setUp(self):
        self.instance = bvhio.readAsBvh('bvhio/tests/example.bvh')

    def test_FrameTime(self):
        self.assertEqual(self.instance.FrameTime, 0.033333)

    def test_FrameCount(self):
        self.assertEqual(self.instance.FrameCount, 2)

class BvhJoint(unittest.TestCase):
    def setUp(self):
        self.instance = bvhio.readAsBvh('bvhio/tests/example.bvh').Root
        self.joints = [ # for j, i, d in root.layout(): print(f"( {d}, glm.{j.Offset}, {j.Channels}, {len(j.Children)}, glm.{j.EndSite}, glm.{j.getTip()}, {j.getLength():09.6f}, glm.{j.getRotation()}, '{j .Name}', ),")
            ( 0, glm.vec3(            0,            0,            0 ), ['Xposition', 'Yposition', 'Zposition', 'Zrotation', 'Xrotation', 'Yrotation'], 3, glm.vec3(            0,            1,            0 ), glm.vec3(            0,      1.73667,            0 ), 01.736667, glm.quat(            1,            0,            0,            0 ), 'Hips', ),
            ( 1, glm.vec3(            0,         5.21,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 3, glm.vec3(            0,            1,            0 ), glm.vec3(            0,      17.0367,      1.24667 ), 17.082216, glm.quat(     0.999333,    0.0365139,            0,            0 ), 'Chest', ),
            ( 2, glm.vec3(            0,        18.65,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,         5.45,            0 ), 05.450000, glm.quat(            1,            0,            0,            0 ), 'Neck', ),
            ( 3, glm.vec3(            0,         5.45,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 0, glm.vec3(            0,         3.87,            0 ), glm.vec3(            0,         3.87,            0 ), 03.870000, glm.quat(            1,            0,            0,            0 ), 'Head', ),
            ( 2, glm.vec3(         1.12,        16.23,         1.87 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(         5.54,            0,            0 ), 05.540000, glm.quat(     0.707107,            0,            0,    -0.707107 ), 'LeftCollar', ),
            ( 3, glm.vec3(         5.54,            0,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -11.96,            0 ), 11.960000, glm.quat(            0,            0,            0,            1 ), 'LeftUpArm', ),
            ( 4, glm.vec3(            0,       -11.96,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,        -9.93,            0 ), 09.930000, glm.quat(            0,            0,            0,            1 ), 'LeftLowArm', ),
            ( 5, glm.vec3(            0,        -9.93,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 0, glm.vec3(            0,           -7,            0 ), glm.vec3(            0,           -7,            0 ), 07.000000, glm.quat(            0,            0,            0,            1 ), 'LeftHand', ),
            ( 2, glm.vec3(        -1.12,        16.23,         1.87 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(        -6.07,            0,            0 ), 06.070000, glm.quat(     0.707107,            0,           -0,     0.707107 ), 'RightCollar', ),
            ( 3, glm.vec3(        -6.07,            0,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -11.82,            0 ), 11.820000, glm.quat(            0,            0,            0,            1 ), 'RightUpArm', ),
            ( 4, glm.vec3(            0,       -11.82,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -10.65,            0 ), 10.650000, glm.quat(            0,            0,            0,            1 ), 'RightLowArm', ),
            ( 5, glm.vec3(            0,       -10.65,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 0, glm.vec3(            0,           -7,            0 ), glm.vec3(            0,           -7,            0 ), 07.000000, glm.quat(            0,            0,            0,            1 ), 'RightHand', ),
            ( 1, glm.vec3(         3.91,            0,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -18.34,            0 ), 18.340000, glm.quat(            0,            0,            0,            1 ), 'LeftUpLeg', ),
            ( 2, glm.vec3(            0,       -18.34,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -17.37,            0 ), 17.370001, glm.quat(            0,            0,            0,            1 ), 'LeftLowLeg', ),
            ( 3, glm.vec3(            0,       -17.37,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 0, glm.vec3(            0,        -3.46,            0 ), glm.vec3(            0,        -3.46,            0 ), 03.460000, glm.quat(            0,            0,            0,            1 ), 'LeftFoot', ),
            ( 1, glm.vec3(        -3.91,            0,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -17.63,            0 ), 17.629999, glm.quat(            0,            0,            0,            1 ), 'RightUpLeg', ),
            ( 2, glm.vec3(            0,       -17.63,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 1, glm.vec3(            0,            1,            0 ), glm.vec3(            0,       -17.14,            0 ), 17.139999, glm.quat(            0,            0,            0,            1 ), 'RightLowLeg', ),
            ( 3, glm.vec3(            0,       -17.14,            0 ), ['Zrotation', 'Xrotation', 'Yrotation'], 0, glm.vec3(            0,        -3.75,            0 ), glm.vec3(            0,        -3.75,            0 ), 03.750000, glm.quat(            0,            0,            0,            1 ), 'RightFoot', ),
        ]
        self.frames = [
            [ [ glm.vec3(         8.03,        35.01,        88.36 ), glm.quat(     0.131166,   -0.0117277,    -0.982546,    -0.131386 ) ], [ glm.vec3(         7.81,         35.1,        86.47 ), glm.quat(     0.108987,   -0.0197806,    -0.987099,    -0.115613 ) ],  ],
            [ [ glm.vec3(            0,         5.21,            0 ), glm.quat(     0.919631,     0.357174,    -0.160325,    0.0316445 ) ], [ glm.vec3(            0,         5.21,            0 ), glm.quat(     0.916321,     0.373837,    -0.140206,    0.0307345 ) ],  ],
            [ [ glm.vec3(            0,        18.65,            0 ), glm.quat(     0.925643,     0.372106,    0.0256287,    0.0637533 ) ], [ glm.vec3(            0,        18.65,            0 ), glm.quat(     0.926374,     0.370617,    0.0248438,    0.0620981 ) ],  ],
            [ [ glm.vec3(            0,         5.45,            0 ), glm.quat(     0.933054,    -0.351756,    0.0585907,   -0.0473785 ) ], [ glm.vec3(            0,         5.45,            0 ), glm.quat(     0.933368,    -0.351521,    0.0529141,   -0.0495629 ) ],  ],
            [ [ glm.vec3(         1.12,        16.23,         1.87 ), glm.quat(     0.992182,  -0.00781711,    0.0886372,    0.0875027 ) ], [ glm.vec3(         1.12,        16.23,         1.87 ), glm.quat(     0.985491,  -0.00602162,    0.0357919,     0.165799 ) ],  ],
            [ [ glm.vec3(         5.54,            0,            0 ), glm.quat(     0.639614,    -0.120021,    -0.165798,     0.740945 ) ], [ glm.vec3(         5.54,            0,            0 ), glm.quat(     0.677778,   0.00159328,    -0.117437,     0.725826 ) ],  ],
            [ [ glm.vec3(            0,       -11.96,            0 ), glm.quat(     0.694325,    -0.714836,   -0.0378194,   -0.0741041 ) ], [ glm.vec3(            0,       -11.96,            0 ), glm.quat(     0.669542,    -0.740189,    0.0610665,    0.0102361 ) ],  ],
            [ [ glm.vec3(            0,        -9.93,            0 ), glm.quat(     0.999982,  0.000261795,  1.57639e-06,   0.00602135 ) ], [ glm.vec3(            0,        -9.93,            0 ), glm.quat(     0.999976,   0.00322879,  1.97238e-05,   0.00610858 ) ],  ],
            [ [ glm.vec3(        -1.12,        16.23,         1.87 ), glm.quat(      0.98834,   -0.0111829,   -0.0908157,    -0.121703 ) ], [ glm.vec3(        -1.12,        16.23,         1.87 ), glm.quat(     0.979149,   -0.0142239,    -0.188732,   -0.0737944 ) ],  ],
            [ [ glm.vec3(        -6.07,            0,            0 ), glm.quat(     0.517563,    -0.581909,    -0.519682,    -0.351341 ) ], [ glm.vec3(        -6.07,            0,            0 ), glm.quat(     0.577333,    -0.624629,       -0.433,     -0.29839 ) ],  ],
            [ [ glm.vec3(            0,       -11.82,            0 ), glm.quat(     0.762976,    -0.606189,     0.177084,     0.138002 ) ], [ glm.vec3(            0,       -11.82,            0 ), glm.quat(     0.778739,    -0.591803,     0.161657,     0.131154 ) ],  ],
            [ [ glm.vec3(            0,       -10.65,            0 ), glm.quat(     0.999888,   0.00602318,  9.20184e-05,   -0.0136991 ) ], [ glm.vec3(            0,       -10.65,            0 ), glm.quat(     0.999864,    0.0082931,  0.000143844,   -0.0142213 ) ],  ],
            [ [ glm.vec3(         3.91,            0,            0 ), glm.quat(     0.971953,     0.202143,    -0.024446,     0.117674 ) ], [ glm.vec3(         3.91,            0,            0 ), glm.quat(     0.984412,      0.13691,   -0.0151918,     0.109352 ) ],  ],
            [ [ glm.vec3(            0,       -18.34,            0 ), glm.quat(     0.894013,     0.411485,     0.106536,     0.141674 ) ], [ glm.vec3(            0,       -18.34,            0 ), glm.quat(       0.8647,     0.490346,    0.0719332,     0.081736 ) ],  ],
            [ [ glm.vec3(            0,       -17.37,            0 ), glm.quat(     0.999951,  -0.00994821,            0,            0 ) ], [ glm.vec3(            0,       -17.37,            0 ), glm.quat(     0.999898,    0.0143112,            0,            0 ) ],  ],
            [ [ glm.vec3(        -3.91,            0,            0 ), glm.quat(     0.985387,   -0.0944943,   -0.0135394,    -0.141065 ) ], [ glm.vec3(        -3.91,            0,            0 ), glm.quat(        0.985,   -0.0903176,   -0.0134328,    -0.146418 ) ],  ],
            [ [ glm.vec3(            0,       -17.63,            0 ), glm.quat(     0.883393,       0.4543,    -0.109673,    0.0346498 ) ], [ glm.vec3(            0,       -17.63,            0 ), glm.quat(     0.884521,     0.457052,   -0.0869551,    0.0341273 ) ],  ],
            [ [ glm.vec3(            0,       -17.14,            0 ), glm.quat(     0.978238,    -0.207485,            0,            0 ) ], [ glm.vec3(            0,       -17.14,            0 ), glm.quat(     0.974507,    -0.224356,            0,            0 ) ],  ],
        ]

    def test_JointCount(self):
        self.assertEqual(len(self.joints), len(self.instance.layout()))

    def test_Depth(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(d, self.joints[i][0])

    def test_Name(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(j.Name, self.joints[i][-1])

    def test_Offset(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(j.Offset, self.joints[i][1])

    def test_Channels(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(j.Channels, self.joints[i][2])

    def test_Children(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(len(j.Children), self.joints[i][3])

    def test_EndSite(self):
        for j, i, d in self.instance.layout():
            self.assertEqual(j.EndSite, self.joints[i][4])

    def test_getTip(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-07, glm.distance2(j.getTip(), self.joints[i][5]))

    def test_getLength(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-05, abs(j.getLength() - self.joints[i][6]))

    def test_getRotation(self):
        for j, i, d in self.instance.layout():
            self.assertGreater(1e-05, deviationQuaternion(j.getRotation(), self.joints[i][7]))

    def test_Keyframes(self):
        for j, i, d in self.instance.layout():
            for frame, pose in enumerate(j.Keyframes):
                self.assertEqual(pose.Position, self.frames[i][frame][0])
                self.assertEqual(pose.Scale, glm.vec3(1))
                self.assertGreater(1e-05, glm.length(pose.Rotation - self.frames[i][frame][1]))
