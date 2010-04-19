import unittest
import mockfs
import mockfs.tests.test_mockfs
import mockfs.tests.test_util


def suite():
    suite = unittest.TestSuite()
    suite.addTest(mockfs.tests.test_mockfs.suite())
    suite.addTest(mockfs.tests.test_util.suite())
    return suite


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    main()
