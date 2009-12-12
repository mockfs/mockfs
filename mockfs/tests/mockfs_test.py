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

    def test_first_level_subdir(self):
        """Test files at the root of the filesystem"""
        mockfs.add_entries({'/foo': 'bar'})
        self.assertTrue(os.path.exists('/'))
        self.assertTrue(os.path.isdir('/'))
        self.assertTrue(os.path.exists('/foo'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MockFSTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
