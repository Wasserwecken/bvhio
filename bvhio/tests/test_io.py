import unittest
import bvhio

class Parser(unittest.TestCase):
    def test_readAsBVH(self):
        data = bvhio.readAsBvh('bvhio/tests/example.bvh')
        self.assertEqual(bvhio.BvhContainer, type(data))
        self.assertEqual(bvhio.BvhJoint, type(data.Root))
        self.assertEqual(data.FrameCount, 2)
        self.assertEqual(data.FrameTime, 0.033333)

    def test_readAsHierarchy(self):
        data = bvhio.readAsHierarchy('bvhio/tests/example.bvh')
        self.assertEqual(bvhio.Joint, type(data))
