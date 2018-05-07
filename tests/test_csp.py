import unittest
import operator

import dwavebinarycsp


class TestCSP(unittest.TestCase):
    def test_add_constraint_function(self):
        csp = dwavebinarycsp.CSP(dwavebinarycsp.BINARY)

        def f(a, b, c): return a * b == c

        csp.add_constraint(f, ['a', 'b', 'c'])

        self.assertTrue(csp.check({'a': 0, 'b': 0, 'c': 0}))
        self.assertFalse(csp.check({'a': 1, 'b': 0, 'c': 1}))

    def test_add_constraint_table_BINARY(self):
        csp = dwavebinarycsp.CSP(dwavebinarycsp.BINARY)

        neq = frozenset([(0, 1), (1, 0)])

        csp.add_constraint(neq, ['a', 'b'])

        self.assertTrue(csp.check({'a': 0, 'b': 1}))
        self.assertTrue(csp.check({'a': 1, 'b': 0}))

        self.assertFalse(csp.check({'a': 0, 'b': 0}))
        self.assertFalse(csp.check({'a': 1, 'b': 1}))

        eq = frozenset([(0, 0), (1, 1)])

        csp.add_constraint(eq, ['b', 'c'])

        self.assertTrue(csp.check({'a': 0, 'b': 1, 'c': 1}))
        self.assertTrue(csp.check({'a': 1, 'b': 0, 'c': 0}))

        self.assertFalse(csp.check({'a': 0, 'b': 0, 'c': 0}))
        self.assertFalse(csp.check({'a': 1, 'b': 1, 'c': 1}))
        self.assertFalse(csp.check({'a': 0, 'b': 1, 'c': 0}))
        self.assertFalse(csp.check({'a': 1, 'b': 0, 'c': 1}))
        self.assertFalse(csp.check({'a': 0, 'b': 0, 'c': 1}))
        self.assertFalse(csp.check({'a': 1, 'b': 1, 'c': 0}))

    def test_fix_variable(self):
        csp = dwavebinarycsp.CSP(dwavebinarycsp.BINARY)

        csp.add_constraint(operator.eq, ['a', 'b'])
        csp.add_constraint(operator.ne, ['b', 'c'])
        csp.add_constraint(operator.eq, ['c', 'd'])

        self.assertTrue(csp.check({'a': 1, 'b': 1, 'c': 0, 'd': 0}))
        self.assertTrue(csp.check({'a': 0, 'b': 0, 'c': 1, 'd': 1}))

        csp.fix_variable('d', 1)

        self.assertTrue(csp.check({'a': 0, 'b': 0, 'c': 1, 'd': 1}))
        self.assertFalse(csp.check({'a': 1, 'b': 1, 'c': 0, 'd': 0}))

        self.assertTrue(csp.check({'a': 0, 'b': 0, 'c': 1}))
