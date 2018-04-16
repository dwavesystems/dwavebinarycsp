import unittest

import dimod

import dwave_constraint_compilers as dcc


class TestGates(unittest.TestCase):
    def check_constraint_form(self, constraint, vartype):
        self.assertIn('feasible_configurations', constraint)
        self.assertIn('name', constraint)
        self.assertIn('variables', constraint)

    def test_AND(self):
        and_ = dcc.constraints.AND(0, 1, 2)
        self.check_constraint_form(and_, dimod.BINARY)
