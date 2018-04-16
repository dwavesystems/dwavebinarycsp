import unittest

import penaltymodel as pm
import networkx as nx
import dimod

try:
    import unittest.mock as mock
except ImportError:
    import mock

import dwave_constraint_compilers as dcc


def get_penalty_model(spec):
    """Assumes that every spec is for an AND gate"""
    # just intercept the things we recognize
    if spec.feasible_configurations == {(-1, -1): 0, (1, 1): 0}:
        # equality
        linear = {v: 0 for v in spec.graph}
        quadratic = {edge: 0 for edge in spec.graph.edges}
        if spec.decision_variables in quadratic:
            quadratic[spec.decision_variables] = -1
        else:
            u, v = spec.decision_variables
            quadratic[(v, u)] = -1
        model = dimod.BinaryQuadraticModel(linear, quadratic, 0, dimod.SPIN)
        return pm.PenaltyModel.from_specification(spec, model, 2, 0)
    elif spec.feasible_configurations == {(-1, 1): 0, (1, -1): 0}:
        # disequality
        linear = {v: 0 for v in spec.graph}
        quadratic = {edge: 0 for edge in spec.graph.edges}
        if spec.decision_variables in quadratic:
            quadratic[spec.decision_variables] = 1
        else:
            u, v = spec.decision_variables
            quadratic[(v, u)] = 1
        model = dimod.BinaryQuadraticModel(linear, quadratic, 0, dimod.SPIN)
        return pm.PenaltyModel.from_specification(spec, model, 2, 0)
    raise NotImplementedError


class TestSatisfy(unittest.TestCase):
    @mock.patch('dwave_constraint_compilers.compilers.stitcher.pm.get_penalty_model',
                side_effect=get_penalty_model)
    def test_typical(self, mock_get_penalty_model):
        constraints = {
            'EQ1': {
                'feasible_configurations': [(0, 0), (1, 1)],
                'variables': ['a', 'b']},
            'EQ2': {
                'feasible_configurations': [(0, 0), (1, 1)],
                'variables': ['c', 'b']},
            'NEQ1': {
                'feasible_configurations': [(0, 1), (1, 0)],
                'variables': ['c', 'e']},
            'NEQ2': {
                'feasible_configurations': [(0, 1), (1, 0)],
                'variables': ['a', 'e']},
        }

        soln = dcc.satisfy(constraints, dimod.ExactSolver())

        # check that constraints wasn't altered
        self.assertEqual(constraints,
                         {'EQ1': {
                             'feasible_configurations': [(0, 0), (1, 1)],
                             'variables': ['a', 'b']},
                          'EQ2': {
                             'feasible_configurations': [(0, 0), (1, 1)],
                             'variables': ['c', 'b']},
                          'NEQ1': {
                             'feasible_configurations': [(0, 1), (1, 0)],
                             'variables': ['c', 'e']},
                          'NEQ2': {
                             'feasible_configurations': [(0, 1), (1, 0)],
                             'variables': ['a', 'e']}})

        self.assertTrue(dcc.is_satisfied(constraints, soln))
