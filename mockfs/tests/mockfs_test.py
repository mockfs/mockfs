import os
import unittest

import mockfs


class MockFSTestCase(unittest.TestCase):
    def setUp(self):
        mockfs.install(entries={})

    def test_empty(self):
        self.assertFalse(os.path.exists('/'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MockFSTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
