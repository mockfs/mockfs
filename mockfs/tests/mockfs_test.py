import os
import unittest

import mockfs


class MockFSTestCase(unittest.TestCase):
    def setUp(self):
        mockfs.install()

    def tearDown(self):
        mockfs.uninstall()

    def test_empty(self):
        """Test an empty filesystem"""
        self.assertFalse(os.path.exists('/'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MockFSTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
