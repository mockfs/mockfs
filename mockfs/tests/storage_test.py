import unittest

# subjects under test
import os

import mockfs


class StorageTestCase(unittest.TestCase):
    def setUp(self):
        self.mfs = mockfs.replace_builtins()

    def tearDown(self):
        mockfs.restore_builtins()

    def _mkfs(self):
        filesystem = {
            '/a/a/b': '/a/a/b',
            '/a/b/b': '/a/b/b',
            '/b/a/b': '/b/a/b',
            '/b/b/b': '/b/b/b',
        }
        self.mfs.add_entries(filesystem)

        for path in filesystem:
            self.assertTrue(os.path.isdir(os.path.dirname(path)))
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isfile(path))

        return filesystem

    def test_open(self):
        filesystem = self._mkfs()

        for path, expected in filesystem.items():
            fh = open(path, 'r')
            data = fh.read()
            fh.close()
            self.assertEqual(data, expected)

    def test_open_with_rogue_paths(self):
        filesystem = self._mkfs()

        for path, expected in filesystem.items():
            fh = open('//' + path.replace('/', '/////'), 'r')
            data = fh.read()
            fh.close()
            self.assertEqual(data, expected)

    def test_open_rw(self):
        self._mkfs()
        expected = 'just another pythonista'

        fh = open('/a/a/b', 'w')
        fh.write(expected)
        fh.close()

        fh = open('/a/a/b', 'r')
        data = fh.read()
        fh.close()

        self.assertEqual(data, expected)

    def test_dir_not_exists(self):
        self.assertRaises(IOError, open, '/does/not/exist', 'w')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StorageTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
