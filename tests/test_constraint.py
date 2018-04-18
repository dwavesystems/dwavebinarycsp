import unittest
import operator
import itertools

import dwavecsp
import dwavecsp.testing as dcspt


class TestConstraint(unittest.TestCase):

    def test_instantiation(self):
        const = dwavecsp.Constraint()

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset())
        self.assertEqual(const.variables, tuple())
        self.assertTrue(const.func())  # should always return true

        with self.assertRaises(AttributeError):
            const.vartype

    def test__len__(self):
        const = dwavecsp.Constraint()

        self.assertEqual(len(const), 0)

        const = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.SPIN)

        self.assertEqual(len(const), 2)

    def test_from_func(self):
        const = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.SPIN)

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, -1), (1, 1)]))
        self.assertEqual(('a', 'b'), const.variables)

    def test_from_configurations(self):
        const = dwavecsp.Constraint.from_configurations([(-1, 1), (1, 1)], ['a', 'b'], dwavecsp.SPIN)

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, 1), (1, 1)]))
        self.assertEqual(const.variables, ('a', 'b'))

    def test_fix_variable(self):
        const = dwavecsp.Constraint.from_configurations([(-1, 1), (1, 1)], ['a', 'b'], dwavecsp.SPIN)

        const.fix_variable('a', -1)

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1,)]))
        self.assertEqual(const.variables, ('b',))

    def test_fix_variable_unsat(self):
        const = dwavecsp.Constraint.from_configurations([(-1, 1), (1, 1)], ['a', 'b'], dwavecsp.SPIN)

        with self.assertRaises(dwavecsp.exceptions.UnsatError):
            const.fix_variable('b', -1)

    def test__or__disjoint(self):
        eq_a_b = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.SPIN)
        ne_c_d = dwavecsp.Constraint.from_func(operator.ne, ['c', 'd'], dwavecsp.SPIN)

        const = eq_a_b | ne_c_d

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.variables, ('a', 'b', 'c', 'd'))

        self.assertTrue(const.check({'a': 0, 'b': 0, 'c': 0, 'd': 0}))  # only eq_a_b is satisfied
        self.assertFalse(const.check({'a': 1, 'b': 0, 'c': 0, 'd': 0}))  # neither satisified

    def test__or__(self):
        eq_a_b = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.SPIN)
        ne_b_c = dwavecsp.Constraint.from_func(operator.ne, ['c', 'b'], dwavecsp.SPIN)

        const = eq_a_b | ne_b_c

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.variables, ('a', 'b', 'c'))

        self.assertTrue(const.check({'a': 0, 'b': 0, 'c': 0}))  # only eq_a_b is satisfied
        self.assertFalse(const.check({'a': 1, 'b': 0, 'c': 0}))  # neither satisfied
        self.assertTrue(const.check({'a': 0, 'b': 1, 'c': 0}))  # only ne_b_c is satisfied

    def test__and__disjoint(self):
        eq_a_b = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.SPIN)
        ne_c_d = dwavecsp.Constraint.from_func(operator.ne, ['c', 'd'], dwavecsp.SPIN)

        const = eq_a_b & ne_c_d

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, -1, -1, 1), (1, 1, -1, 1),
                                                          (-1, -1, 1, -1), (1, 1, 1, -1)]))
        self.assertEqual(const.variables, ('a', 'b', 'c', 'd'))

    def test__and__(self):
        eq_a_b = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.SPIN)
        ne_b_c = dwavecsp.Constraint.from_func(operator.ne, ['c', 'b'], dwavecsp.SPIN)

        const = eq_a_b & ne_b_c

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, -1, 1), (1, 1, -1)]))
        self.assertEqual(const.variables, ('a', 'b', 'c'))
