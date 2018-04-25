import unittest
import operator

# try:
#     import unittest.mock as mock
# except ImportError:
#     import mock

import networkx as nx
# import penaltymodel as pm
# import dimod

import dwavecsp
from dwavecsp.compilers import stitcher


class TestStitch(unittest.TestCase):
    def test_iter_complete_graph_simple(self):

        graphs = list(stitcher.iter_complete_graphs(4, 6))
        self.assertEqual(len(graphs), 2)

        self.assertEqual(graphs[0].adj, nx.complete_graph(4).adj)
        self.assertEqual(graphs[1].adj, nx.complete_graph(5).adj)

    def test_iter_complete_graph_seed_nodes(self):

        # implicit that the length is 2
        G0, G1 = stitcher.iter_complete_graphs(['a', 'b'], 4)

        self.assertIn('a', G0)
        self.assertIn('a', G1)
        self.assertIn('b', G0)
        self.assertIn('b', G1)

        self.assertEqual(set(G1), {'a', 'b', 0})  # aux var should be index-labeled

    def test_iter_complete_graph_seed_node_index(self):

        # implicit that the length is 3
        G0, G1, G2 = stitcher.iter_complete_graphs([1], 4)

        self.assertIn(1, G0)
        self.assertIn(1, G1)

        self.assertEqual(set(G0), {1})  # start with label 1
        self.assertEqual(set(G1), {0, 1})
        self.assertEqual(set(G2), {0, 1, 2})

    def test_iter_complete_graph_empty(self):

        # should produce empty lists rather than failing
        self.assertFalse(list(stitcher.iter_complete_graphs(['a', 'b', 'c'], 2)))
        self.assertFalse(list(stitcher.iter_complete_graphs(3, 2)))

    def test_iter_complete_graph_factory(self):

        def factory():
            i = 0
            while True:
                yield 'aux{}'.format(i)
                i += 1

        G0, G1, G2 = stitcher.iter_complete_graphs(['a', 'b'], 5, factory=factory())

        self.assertEqual(set(G2), {'a', 'b', 'aux0', 'aux1'})


    # @mock.patch('dwavecsp.compilers.stitcher.pm.get_penalty_model')
    # def test_make_widgets_from(self, mock_get_penalty_model):
    #     # we want to make get_penalty_model return an object we can treat
    #     # as a signal
    #     signal = object()
    #     mock_get_penalty_model.return_value = signal

    #     # if we give one constraint, should get back a list of exactly one signal
    #     constraints = [dwavecsp.generators.AND('a', 'b', 'c', dwavecsp.BINARY)]
    #     pmodels = list(stitcher.iter_penalty_models(constraints))
    #     self.assertEqual(pmodels, [signal])

        # # now two constraints
        # constraints['INVERT'] = {'feasible_configurations': [(0, 1), (1, 0)],
        #                          'variables': [3, 0]}
        # widgets = stitcher.make_widgets_from(constraints)
        # self.assertEqual(widgets, [signal, signal])

    # @mock.patch('dwave_constraint_compilers.compilers.stitcher.pm.get_penalty_model')
    # def test_make_widgets_from_impossible_model(self, mock_get_penalty_model):
    #     # we want to make get_penalty_model to always raise the ImpossibleModelError
    #     signal = object()
    #     mock_get_penalty_model.side_effect = pm.ImpossiblePenaltyModel

    #     # if we give one constraint, should get back a list of exactly one signal
    #     constraints = {
    #         'AND': {
    #             'feasible_configurations': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0)],
    #             'variables': [0, 1, 2]
    #         }
    #     }
    #     # in this case we should get a runtime error saying that the model cannot be built
    #     with self.assertRaises(RuntimeError):
    #         widgets = stitcher.make_widgets_from(constraints)

    # def test_stitch(self):
    #     constraints = {
    #         'gate': {
    #             'feasible_configurations': [(0, 0, 0)],
    #             'variables': [0, 1, 2]
    #         }
    #     }
    #     linear = {0: -1, 1: -1, 2: -1}
    #     quadratic = {(0, 1): -1, (0, 2): -1, (1, 2): -1}
    #     offset = 0
    #     expected_bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.SPIN)
    #     mock_pm = mock.MagicMock()
    #     mock_pm.model = expected_bqm
    #     stitcher.pm.get_penalty_model = mock.MagicMock(return_value=mock_pm)

    #     self.assertEqual(expected_bqm, stitcher.stitch(constraints))

    # def test_stitch_multiple_constraints(self):
    #     constraints = {
    #         'gate1': {
    #             'feasible_configurations': [(0, 0, 0)],
    #             'variables': [0, 1, 2]
    #         },
    #         'gate2': {
    #             'feasible_configurations': [(0, 0, 0)],
    #             'variables': [0, 1, 2]
    #         }
    #     }

    #     linear = {0: -1, 1: -1, 2: -1}
    #     quadratic = {(0, 1): -1, (0, 2): -1, (1, 2): -1}
    #     offset = 1
    #     mock_bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.SPIN)
    #     mock_pm = mock.MagicMock()
    #     mock_pm.model = mock_bqm
    #     stitcher.pm.get_penalty_model = mock.MagicMock(return_value=mock_pm)

    #     linear = {0: -2, 1: -2, 2: -2}
    #     quadratic = {(0, 1): -2, (0, 2): -2, (1, 2): -2}
    #     offset = 2
    #     expected_bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.SPIN)
    #     self.assertEqual(expected_bqm, stitcher.stitch(constraints))

    # @mock.patch('dwave_constraint_compilers.compilers.stitcher.pm.get_penalty_model')
    # def test_stitch_constraint_propgation(self, mock_get_penalty_model):
    #     def is_and(spec):
    #         self.assertEqual(spec.feasible_configurations,
    #                          {(-1, -1, -1): 0, (-1, 1, -1): 0, (1, -1, -1): 0, (1, 1, 1): 0})
    #         return mock.MagicMock()

    #     mock_get_penalty_model.side_effect = is_and

    #     constraints = {
    #         'AND': {
    #             'feasible_configurations': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)],
    #             'variables': [0, 1, 2]
    #         }
    #     }

    #     stitcher.stitch(constraints)


if __name__ == '__main__':
    unittest.main()
