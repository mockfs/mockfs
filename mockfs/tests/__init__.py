import unittest
import mockfs
import mockfs.tests.mockfs_test


def suite():
    suite = unittest.TestSuite()
    suite.addTest(mockfs.tests.mockfs_test.suite())
    return suite


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    main()
