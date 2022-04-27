# encoding: utf-8
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

import dimod
import networkx as nx

import dwavebinarycsp


class TestDocumentation(unittest.TestCase):
    def test_intro_example(self):
        # Dev note: test that the example in the intro documentation still works, if this fails go
        # update the example!

        # from dwave.system.samplers import DWaveSampler
        # from dwave.system.composites import EmbeddingComposite
        # import networkx as nx
        # import matplotlib.pyplot as plt

        # Represent the map as the nodes and edges of a graph
        provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
        neighbors = [('AB', 'BC'), ('AB', 'NT'), ('AB', 'SK'), ('BC', 'NT'), ('BC', 'YT'), ('MB', 'NU'),
                     ('MB', 'ON'), ('MB', 'SK'), ('NB', 'NS'), ('NB', 'QC'), ('NL', 'QC'), ('NT', 'NU'),
                     ('NT', 'SK'), ('NT', 'YT'), ('ON', 'QC')]

        # Function for the constraint that two nodes with a shared edge not both select one color
        def not_both_1(v, u):
            return not (v and u)

        # # Function that plots a returned sample
        # def plot_map(sample):
        #     G = nx.Graph()
        #     G.add_nodes_from(provinces)
        #     G.add_edges_from(neighbors)
        #     # Translate from binary to integer color representation
        #     color_map = {}
        #     for province in provinces:
        #           for i in range(colors):
        #             if sample[province+str(i)]:
        #                 color_map[province] = i
        #     # Plot the sample with color-coded nodes
        #     node_colors = [color_map.get(node) for node in G.nodes()]
        #     nx.draw_circular(G, with_labels=True, node_color=node_colors, node_size=3000, cmap=plt.cm.rainbow)
        #     plt.show()

        # Valid configurations for the constraint that each node select a single color
        one_color_configurations = {(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)}
        colors = len(one_color_configurations)

        # Create a binary constraint satisfaction problem
        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

        # Add constraint that each node (province) select a single color
        for province in provinces:
            variables = [province+str(i) for i in range(colors)]
            csp.add_constraint(one_color_configurations, variables)

        # Add constraint that each pair of nodes with a shared edge not both select one color
        for neighbor in neighbors:
            v, u = neighbor
            for i in range(colors):
                variables = [v+str(i), u+str(i)]
                csp.add_constraint(not_both_1, variables)

        # Convert the binary constraint satisfaction problem to a binary quadratic model
        bqm = dwavebinarycsp.stitch(csp)

        sampler = dimod.SimulatedAnnealingSampler()
        # # Set up a solver using the local system’s default D-Wave Cloud Client configuration file
        # # and sample 50 times
        # sampler = EmbeddingComposite(DWaveSampler())         # doctest: +SKIP
        response = sampler.sample(bqm, num_reads=10)

        # # Plot the lowest-energy sample if it meets the constraints
        sample = response.first.sample      # doctest: +SKIP
        # if not csp.check(sample):              # doctest: +SKIP
        #     print("Failed to color map")
        # else:
        #     plot_map(sample)

        if not csp.check(sample):
            pass
