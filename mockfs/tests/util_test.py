import unittest

from mockfs import util


class MockFSUtilTestCase(unittest.TestCase):
    def test_sanitize(self):
        """Test sanitize() with rogue paths"""
        self.assertEqual(util.sanitize('///'), '/')
        self.assertEqual(util.sanitize('///usr//bin///'), '/usr/bin')
        self.assertEqual(util.sanitize('///usr//bin'), '/usr/bin')

    def test_build_nested_dict(self):
        nested = util.build_nested_dict({'/foo': 'bar',
                                         '/a/b/c': 'c'})
        self.assertEqual(nested['foo'], 'bar')
        self.assertEqual(nested['a'], {'b': {'c': 'c'}})

    def test_build_nested_dir_dict(self):
        nested = util.build_nested_dir_dict('/foo')
        self.assertEqual(nested['foo'], {})

        nested = util.build_nested_dir_dict('/bar/baz')
        self.assertEqual(nested['bar']['baz'], {})

    def test_merge_extends_lists(self):
        a = {'a': [1, 2]}
        b = {'a': [3, 4]}
        util.merge_dicts(a, b)
        self.assertEqual(b['a'], [3, 4, 1, 2])

    def test_merge_overrides(self):
        a = {'a': 1}
        b = {'a': 2}
        util.merge_dicts(a, b)
        self.assertEqual(b['a'], 1)

    def test_merge_no_overlap(self):
        a = {'a': 1}
        b = {'b': 2}
        util.merge_dicts(a, b)
        self.assertEqual(b['a'], 1)
        self.assertEqual(b['b'], 2)

    def test_merge_conflict_dicts(self):
        src = {'a': {'b': 'src'}}
        dst = {'a': {'b': 'dst'}}

        util.merge_dicts(src, dst)
        self.assertEqual(dst['a']['b'], 'src')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MockFSUtilTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
