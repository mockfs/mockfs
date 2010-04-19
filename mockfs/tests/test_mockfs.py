import os
import unittest

import mockfs
import mockfs.mfs as mfs


class MockFSTestCase(unittest.TestCase):
    def setUp(self):
        self.mfs = mockfs.install()

    def tearDown(self):
        mockfs.uninstall()

    def test_empty(self):
        """Test an empty filesystem"""
        self.assertFalse(os.path.exists('/'))

    def test_first_level_subdir(self):
        """Test files at the root of the filesystem"""
        self.mfs.add_entries({'/foo': 'bar'})
        self.assertTrue(os.path.exists('/'))
        self.assertTrue(os.path.isdir('/'))
        self.assertTrue(os.path.exists('/foo'))

    def test_nested_directories(self):
        """Test files in subdirectories."""
        filesystem = {
            '/a/a/a': '',
            '/a/a/b': '',
            '/a/b/a': '',
            '/a/b/b': '',
            '/b/a/a': '',
            '/b/a/b': '',
            '/b/b/a': '',
            '/b/b/b': '',
        }
        self.mfs.add_entries(filesystem)

        for path in filesystem:
            self.assertTrue(os.path.isdir(os.path.dirname(path)))
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isfile(path))

    def test_unsanitized_entries(self):
        """Test add_entries() with unsantized paths"""
        self.mfs.add_entries({'///just////another////pythonista': ''})

        self.assertTrue(os.path.isdir('/just'))
        self.assertTrue(os.path.isdir('/just/another'))
        self.assertTrue(os.path.exists('/just/another/pythonista'))
        self.assertTrue(os.path.isfile('/just/another/pythonista'))

    def test_predicates_on_unsanitized_paths(self):
        """Test isdir(), isfile() and exists() on unsanitized paths"""
        self.mfs.add_entries({'/just/another/pythonista': ''})

        self.assertTrue(os.path.isdir('///just'))
        self.assertTrue(os.path.isdir('///just/////another'))
        self.assertTrue(os.path.exists('///just////another////////pythonista'))
        self.assertTrue(os.path.isfile('///just////another////////pythonista'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MockFSTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
