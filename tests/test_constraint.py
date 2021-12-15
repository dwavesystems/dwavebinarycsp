# Copyright 2018 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest
import operator
import itertools

import dwavebinarycsp
import dwavebinarycsp.testing as dcspt


class TestConstraint(unittest.TestCase):

    def test__len__(self):

        const = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)
        dcspt.assert_consistent_constraint(const)
        self.assertEqual(len(const), 2)

    def test_from_func(self):
        const = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, -1), (1, 1)]))
        self.assertEqual(('a', 'b'), const.variables)

    def test_from_configurations(self):
        const = dwavebinarycsp.Constraint.from_configurations([(-1, 1), (1, 1)], ['a', 'b'], dwavebinarycsp.SPIN)

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, 1), (1, 1)]))
        self.assertEqual(const.variables, ('a', 'b'))

    def test_fix_variable(self):
        const = dwavebinarycsp.Constraint.from_configurations([(-1, 1), (1, 1)], ['a', 'b'], dwavebinarycsp.SPIN)

        const.fix_variable('a', -1)

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1,)]))
        self.assertEqual(const.variables, ('b',))

    def test_fix_variable_unsat(self):
        const = dwavebinarycsp.Constraint.from_configurations([(-1, 1), (1, 1)], ['a', 'b'], dwavebinarycsp.SPIN)

        with self.assertRaises(dwavebinarycsp.exceptions.UnsatError):
            const.fix_variable('b', -1)

    def test__or__disjoint(self):
        eq_a_b = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)
        ne_c_d = dwavebinarycsp.Constraint.from_func(operator.ne, ['c', 'd'], dwavebinarycsp.SPIN)

        const = eq_a_b | ne_c_d

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.variables, ('a', 'b', 'c', 'd'))

        self.assertTrue(const.check({'a': 0, 'b': 0, 'c': 0, 'd': 0}))  # only eq_a_b is satisfied
        self.assertFalse(const.check({'a': 1, 'b': 0, 'c': 0, 'd': 0}))  # neither satisified

    def test__or__(self):
        eq_a_b = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)
        ne_b_c = dwavebinarycsp.Constraint.from_func(operator.ne, ['c', 'b'], dwavebinarycsp.SPIN)

        const = eq_a_b | ne_b_c

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.variables, ('a', 'b', 'c'))

        self.assertTrue(const.check({'a': 0, 'b': 0, 'c': 0}))  # only eq_a_b is satisfied
        self.assertFalse(const.check({'a': 1, 'b': 0, 'c': 0}))  # neither satisfied
        self.assertTrue(const.check({'a': 0, 'b': 1, 'c': 0}))  # only ne_b_c is satisfied

    def test__and__disjoint(self):
        eq_a_b = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)
        ne_c_d = dwavebinarycsp.Constraint.from_func(operator.ne, ['c', 'd'], dwavebinarycsp.SPIN)

        const = eq_a_b & ne_c_d

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, -1, -1, 1), (1, 1, -1, 1),
                                                          (-1, -1, 1, -1), (1, 1, 1, -1)]))
        self.assertEqual(const.variables, ('a', 'b', 'c', 'd'))

    def test__and__(self):
        eq_a_b = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)
        ne_b_c = dwavebinarycsp.Constraint.from_func(operator.ne, ['c', 'b'], dwavebinarycsp.SPIN)

        const = eq_a_b & ne_b_c

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(-1, -1, 1), (1, 1, -1)]))
        self.assertEqual(const.variables, ('a', 'b', 'c'))

    def test_negate_variables_binary(self):
        const = dwavebinarycsp.Constraint.from_configurations([(0, 1), (1, 0)], ['a', 'b'], vartype=dwavebinarycsp.BINARY)

        const.flip_variable('a')

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1, 1), (0, 0)]))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(0, 1), (1, 0)], ['a', 'b'], vartype=dwavebinarycsp.BINARY)

        const.flip_variable('b')

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1, 1), (0, 0)]))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(0, 1, 1), (1, 0, 0)],
                                                        ['a', 'b', 'c'],
                                                        vartype=dwavebinarycsp.BINARY)

        const.flip_variable('b')

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1, 1, 0), (0, 0, 1)]))

    def test_negate_variables_spi(self):
        const = dwavebinarycsp.Constraint.from_configurations([(-1, 1), (1, -1)], ['a', 'b'], vartype=dwavebinarycsp.SPIN)

        const.flip_variable('a')

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1, 1), (-1, -1)]))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(-1, 1), (1, -1)], ['a', 'b'], vartype=dwavebinarycsp.SPIN)

        const.flip_variable('b')

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1, 1), (-1, -1)]))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(-1, 1, 1), (1, -1, -1)],
                                                        ['a', 'b', 'c'],
                                                        vartype=dwavebinarycsp.SPIN)

        const.flip_variable('b')

        dcspt.assert_consistent_constraint(const)

        self.assertEqual(const.configurations, frozenset([(1, 1, -1), (-1, -1, 1)]))

    def test_construction_typechecking(self):

        # not function
        with self.assertRaises(TypeError):
            dwavebinarycsp.Constraint(1, {}, [], dwavebinarycsp.BINARY)

        def f():
            pass

        # mismatched lengths
        with self.assertRaises(ValueError):
            dwavebinarycsp.Constraint(f, {tuple(), (1,)}, [], dwavebinarycsp.BINARY)
        with self.assertRaises(ValueError):
            dwavebinarycsp.Constraint(f, {(0,), (1,)}, ['a', 'b'], dwavebinarycsp.BINARY)

        # bad vartype
        with self.assertRaises(ValueError):
            dwavebinarycsp.Constraint(f, {(-1,), (0,)}, ['a'], dwavebinarycsp.BINARY)

    def test_copy(self):
        const = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)
        new_const = const.copy()

        self.assertEqual(const, new_const)
        self.assertIsNot(const, new_const)

    def test_projection_identity(self):
        const = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)

        proj = const.projection(['a', 'b'])

        self.assertEqual(const, proj)
        self.assertIsNot(const, proj)

    def test_projection_unknown_variables(self):
        const = dwavebinarycsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavebinarycsp.SPIN)

        with self.assertRaises(ValueError):
            proj = const.projection(['a', 'c'])

    def test_projection_reducible(self):
        const = dwavebinarycsp.Constraint.from_configurations([(0, 0), (0, 1)], ['a', 'b'], dwavebinarycsp.BINARY)

        a = dwavebinarycsp.Constraint.from_configurations([(0,)], ['a'], dwavebinarycsp.BINARY)
        b = dwavebinarycsp.Constraint.from_configurations([(0,), (1,)], ['b'], dwavebinarycsp.BINARY)

        self.assertEqual(const.projection(['b']), b)
        self.assertEqual(const.projection(['a']), a)
