import unittest

import mockfs.tests.mockfs_test
import mockfs.tests.storage_test
import mockfs.tests.util_test


def suite():
    suite = unittest.TestSuite()
    suite.addTest(mockfs.tests.mockfs_test.suite())
    suite.addTest(mockfs.tests.storage_test.suite())
    suite.addTest(mockfs.tests.util_test.suite())
    return suite


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    main()
