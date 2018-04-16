import unittest

import dimod

from dwave_constraint_compilers import utils


class TestUtils(unittest.TestCase):
    def test_convert_constraint_spin(self):
        constraint = {
            'feasible_configurations': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
            'variables': [0, 1, 2]
        }
        constraint = utils.convert_constraint(constraint)
        self.assertEqual(constraint['feasible_configurations'], [(-1, -1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)])

    def test_convert_constraint_binary(self):
        constraint = {
            'feasible_configurations': [(-1, -1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)],
            'variables': [0, 1, 2]
        }
        constraint = utils.convert_constraint(constraint, vartype=dimod.BINARY)
        self.assertEqual(constraint['feasible_configurations'], [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)])

    def test_convert_sample_spin(self):
        sample = {'a': 1, 'b': 0, 'c': 0}
        sample = utils.convert_sample(sample, vartype=dimod.SPIN)
        self.assertEqual(sample, {'a': 1, 'b': -1, 'c': -1})

    def test_convert_sample_binary(self):
        sample = {'a': 1, 'b': -1, 'c': -1}
        sample = utils.convert_sample(sample, vartype=dimod.BINARY)
        self.assertEqual(sample, {'a': 1, 'b': 0, 'c': 0})

    def test_constraint_vartype(self):
        constraint = {
            'feasible_configurations': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), dimod.BINARY)

        constraint = {
            'feasible_configurations': [(1, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), dimod.BINARY)

        constraint = {
            'feasible_configurations': [(-1, -1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), dimod.SPIN)

        constraint = {
            'feasible_configurations': [(-1, -1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), dimod.SPIN)

        constraint = {
            'feasible_configurations': [(-1, -1, -1), (0, 1, 0), (1, -1, -1), (-1, -1, -1)],
            'variables': [0, 1, 2]
        }
        with self.assertRaises(ValueError):
            utils.constraint_vartype(constraint)

    def test_sample_vartype(self):
        sample = {'a': -1, 'b': +1}
        self.assertIs(utils.sample_vartype(sample), dimod.SPIN)

        # should default to spin
        sample = {'a': +1, 'b': +1}
        self.assertIs(utils.sample_vartype(sample), dimod.SPIN)

        sample = {'a': 0, 'b': +1}
        self.assertIs(utils.sample_vartype(sample), dimod.BINARY)

        with self.assertRaises(ValueError):
            sample = {'a': 0, 'b': -1}
            utils.sample_vartype(sample)

        with self.assertRaises(ValueError):
            sample = {'a': 3}
            utils.sample_vartype(sample)
