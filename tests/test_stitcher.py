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
#
# ================================================================================================

import unittest
import operator
import itertools

import networkx as nx
import dimod

import dwavebinarycsp
from dwavebinarycsp.compilers import stitcher


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

    def test__bqm_from_1sat(self):
        const = dwavebinarycsp.Constraint.from_configurations([(0,)], ['a'], dwavebinarycsp.BINARY)

        bqm = stitcher._bqm_from_1sat(const)

        self.assertTrue(bqm.energy({'a': 0}) + 2 <= bqm.energy({'a': 1}))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(1,)], ['a'], dwavebinarycsp.BINARY)

        bqm = stitcher._bqm_from_1sat(const)

        self.assertTrue(bqm.energy({'a': 1}) + 2 <= bqm.energy({'a': 0}))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(-1,)], ['a'], dwavebinarycsp.SPIN)

        bqm = stitcher._bqm_from_1sat(const)

        self.assertTrue(bqm.energy({'a': -1}) + 2 <= bqm.energy({'a': 1}))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(+1,)], ['a'], dwavebinarycsp.SPIN)

        bqm = stitcher._bqm_from_1sat(const)

        self.assertTrue(bqm.energy({'a': 1}) + 2 <= bqm.energy({'a': -1}))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(-1,), (+1,)], ['a'], dwavebinarycsp.SPIN)

        bqm = stitcher._bqm_from_1sat(const)

        self.assertAlmostEqual(bqm.energy({'a': -1}), bqm.energy({'a': 1}))

        #

        const = dwavebinarycsp.Constraint.from_configurations([(0,), (1,)], ['a'], dwavebinarycsp.BINARY)

        bqm = stitcher._bqm_from_1sat(const)

        self.assertAlmostEqual(bqm.energy({'a': 0}), bqm.energy({'a': 1}))

    def test__bqm_from_2set_BINARY(self):

        # all configs of length 2
        all_binary_configurations = {(i, j) for i in range(2) for j in range(2)}

        # for all possible 2-variable constraints
        for configurations in powerset(all_binary_configurations):
            if not configurations:
                continue

            const = dwavebinarycsp.Constraint.from_configurations(configurations, ['a', 'b'], dimod.BINARY)

            bqm = stitcher._bqm_from_2sat(const)

            ground_energies = set(bqm.energy(dict(zip(['a', 'b'], config))) for config in configurations)

            self.assertEqual(len(ground_energies), 1, 'expected only one ground energy for {}, instead recieved {}'.format(const, ground_energies))

            ground = ground_energies.pop()

            for config in all_binary_configurations:
                if config in configurations:
                    continue
                self.assertGreaterEqual(bqm.energy(dict(zip(['a', 'b'], config))), ground + 2.0)

    def test__bqm_from_2set_SPIN(self):

        # all configs of length 2
        all_binary_configurations = {(i, j) for i in (-1, 1) for j in (-1, 1)}

        # for all possible 2-variable constraints
        for configurations in powerset(all_binary_configurations):
            if not configurations:
                continue

            const = dwavebinarycsp.Constraint.from_configurations(configurations, ['a', 'b'], dimod.SPIN)

            bqm = stitcher._bqm_from_2sat(const)

            ground_energies = set(bqm.energy(dict(zip(['a', 'b'], config))) for config in configurations)

            self.assertEqual(len(ground_energies), 1, 'expected only one ground energy for {}, instead recieved {}'.format(const, ground_energies))

            ground = ground_energies.pop()

            for config in all_binary_configurations:
                if config in configurations:
                    continue
                self.assertGreaterEqual(bqm.energy(dict(zip(['a', 'b'], config))), ground + 2.0)

    def test_stitch_2sat(self):
        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)
        for v in range(10):
            csp.add_constraint(operator.eq, [v, v+1])

        bqm = stitcher.stitch(csp)

        self.assertTrue(all(bias == -1 for bias in bqm.quadratic.values()))
        self.assertTrue(all(bias == 0 for bias in bqm.linear.values()))

    def test_stitch_max_graph_size_is_1(self):
        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

        csp.add_constraint(operator.eq, ['a', 'b'])
        csp.add_constraint(operator.ne, ['b', 'c'])

        with self.assertRaises(dwavebinarycsp.exceptions.ImpossibleBQM):
            bqm = dwavebinarycsp.stitch(csp, max_graph_size=1)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


if __name__ == '__main__':
    unittest.main()
