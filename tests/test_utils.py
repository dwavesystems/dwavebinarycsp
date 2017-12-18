import unittest

import penaltymodel as pm

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
        constraint = utils.convert_constraint(constraint, vartype=pm.BINARY)
        self.assertEqual(constraint['feasible_configurations'], [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)])

    def test_convert_sample_spin(self):
        sample = {'a': 1, 'b': 0, 'c': 0}
        sample = utils.convert_sample(sample, vartype=pm.SPIN)
        self.assertEqual(sample, {'a': 1, 'b': -1, 'c': -1})

    def test_convert_sample_binary(self):
        sample = {'a': 1, 'b': -1, 'c': -1}
        sample = utils.convert_sample(sample, vartype=pm.BINARY)
        self.assertEqual(sample, {'a': 1, 'b': 0, 'c': 0})

    def test_constraint_vartype(self):
        constraint = {
            'feasible_configurations': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), pm.BINARY)

        constraint = {
            'feasible_configurations': [(1, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), pm.BINARY)

        constraint = {
            'feasible_configurations': [(-1, -1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), pm.SPIN)

        constraint = {
            'feasible_configurations': [(-1, -1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)],
            'variables': [0, 1, 2]
        }
        self.assertEqual(utils.constraint_vartype(constraint), pm.SPIN)



if __name__ == '__main__':
    unittest.main()
