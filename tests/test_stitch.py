import unittest
import networkx as nx
import string
from unittest.mock import patch, MagicMock
from dwave_constraint_compilers.compilers import stitcher
from penaltymodel import BinaryQuadraticModel, SPIN


class TestStitch(unittest.TestCase):

    def test_make_complete_graph_all_decision_vars(self):
        n = 10
        vertices = list(string.ascii_lowercase[:n])

        edges = set({})
        for i, u in enumerate(vertices):
            for v in vertices[i + 1:]:
                edges.add((u, v))

        expected_graph = nx.Graph()
        expected_graph.add_edges_from(edges)

        result = stitcher.make_complete_graph_from(vertices, n)
        self.assertEqual(expected_graph.nodes(), result.nodes())
        self.assertEqual(expected_graph.edges(), result.edges())

    def test_make_complete_graph_more_nodes_than_vars(self):
        n = 10
        vertices = list(string.ascii_lowercase[:(n - 5)])

        edges = set({})
        all_vertices = vertices + list(range(len(vertices), n))
        for i, u in enumerate(all_vertices):
            for v in all_vertices[i + 1:]:
                edges.add((u, v))

        expected_graph = nx.Graph()
        expected_graph.add_edges_from(edges)

        result = stitcher.make_complete_graph_from(vertices, n)
        self.assertEqual(expected_graph.nodes(), result.nodes())
        self.assertEqual(expected_graph.edges(), result.edges())

    def test_make_complete_graph_less_nodes_than_vars(self):
        n = 5
        vertices = list(string.ascii_lowercase[:(n + 5)])

        with self.assertRaises(RuntimeError):
            stitcher.make_complete_graph_from(vertices, n)

    @patch('stitcher.pm.get_penalty_model', return_value='mock')
    def test_make_widgets(self, pm):
        constraints = {
            'AND': {
                'feasible_configurations': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
                'variables': [0, 1, 2]
            }
        }
        widgets = stitcher.make_widgets_from(constraints)
        self.assertEqual(widgets, ['mock'])

    def test_stitch(self):
        constraints = {
            'gate': {
                'feasible_configurations': [(0, 0, 0)],
                'variables': [0, 1, 2]
            }
        }
        linear = {0: -1, 1: -1, 2: -1}
        quadratic = {(0, 1): -1, (0, 2): -1, (1, 2): -1}
        offset = 0
        expected_bqm = BinaryQuadraticModel(linear, quadratic, offset, SPIN)
        mock_pm = MagicMock()
        mock_pm.model = expected_bqm
        stitcher.pm.get_penalty_model = MagicMock(return_value=mock_pm)

        self.assertEqual(expected_bqm, stitcher.stitch(constraints))

    def test_stitch_multiple_constraints(self):
        constraints = {
            'gate1': {
                'feasible_configurations': [(0, 0, 0)],
                'variables': [0, 1, 2]
            },
            'gate2': {
                'feasible_configurations': [(0, 0, 0)],
                'variables': [0, 1, 2]
            }
        }

        linear = {0: -1, 1: -1, 2: -1}
        quadratic = {(0, 1): -1, (0, 2): -1, (1, 2): -1}
        offset = 1
        mock_bqm = BinaryQuadraticModel(linear, quadratic, offset, SPIN)
        mock_pm = MagicMock()
        mock_pm.model = mock_bqm
        stitcher.pm.get_penalty_model = MagicMock(return_value=mock_pm)

        linear = {0: -2, 1: -2, 2: -2}
        quadratic = {(0, 1): -2, (0, 2): -2, (1, 2): -2}
        offset = 2
        expected_bqm = BinaryQuadraticModel(linear, quadratic, offset, SPIN)
        self.assertEqual(expected_bqm, stitcher.stitch(constraints))


if __name__ == '__main__':
    unittest.main()
