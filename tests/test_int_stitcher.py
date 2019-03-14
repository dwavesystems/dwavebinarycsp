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
#
# ================================================================================================

import unittest
import operator

import dimod

import dwavebinarycsp

import penaltymodel.core as pm


class TestStitch(unittest.TestCase):

    def test_stitch_multiplication_circuit(self):

        circuit = dwavebinarycsp.factories.multiplication_circuit(3)  # 3x3=6 bit

        # the circuit csp is too large for dimod's exact solver to solve quickly, so let's go ahead
        # and fix the inputs and outputs to ones that satisfy the csp and solve for the aux variables

        # 15 = 3 * 5

        fixed_variables = dict([('p0', 1), ('p1', 1), ('p2', 1), ('p3', 1), ('p4', 0), ('p5', 0),  # 15
                                ('a0', 1), ('a1', 1), ('a2', 0),  # 3
                                ('b0', 1), ('b1', 0), ('b2', 1)])  # 5

        for v, val in fixed_variables.items():
            circuit.fix_variable(v, val)

        # original circuit
        original_circuit = dwavebinarycsp.factories.multiplication_circuit(3)

        # we are using an exact solver, so we only need a positive classical gap
        bqm = dwavebinarycsp.stitch(circuit, min_classical_gap=.1)

        resp = dimod.ExactSolver().sample(bqm)

        ground_energy = min(resp.record['energy'])

        for sample, energy in resp.data(['sample', 'energy']):
            if energy == ground_energy:
                self.assertTrue(circuit.check(sample))
            else:
                self.assertFalse(circuit.check(sample))

            # check against the original circuit
            fixed = fixed_variables.copy()
            fixed.update(sample)

            if energy == ground_energy:
                self.assertTrue(original_circuit.check(fixed))
            else:
                self.assertFalse(original_circuit.check(fixed))

    def test_csp_one_xor(self):

        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

        variables = ['a', 'b', 'c']
        xor = dwavebinarycsp.factories.constraint.gates.xor_gate(variables)
        csp.add_constraint(xor)
        bqm = dwavebinarycsp.stitch(csp)

        resp = dimod.ExactSolver().sample(bqm)

        ground_energy = min(resp.record['energy'])

        for sample, energy in resp.data(['sample', 'energy']):
            if energy == ground_energy:
                self.assertTrue(csp.check(sample))
            else:
                if abs(energy - ground_energy) < 2:
                    # if classical gap is less than 2
                    self.assertTrue(csp.check(sample))

    def test_csp_one_xor_impossible(self):

        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

        variables = ['a', 'b', 'c']
        xor = dwavebinarycsp.factories.constraint.gates.xor_gate(variables)
        csp.add_constraint(xor)

        with self.assertRaises(pm.ImpossiblePenaltyModel):
            bqm = dwavebinarycsp.stitch(csp, max_graph_size=3)

    def test_eight_variable_constraint_smoketest(self):

        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

        variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # this is reducible but for our purposes here that's fine
        def f(a, b, c, d, e, f, g, h):
            if a and b:
                return False
            if c and d:
                return False
            if e and f:
                return False
            return not (g and h)

        csp.add_constraint(f, variables)

        bqm = dwavebinarycsp.stitch(csp)

        resp = dimod.ExactSolver().sample(bqm)

        ground_energy = min(resp.record['energy'])

        for sample, energy in resp.data(['sample', 'energy']):
            if energy == ground_energy:
                self.assertTrue(csp.check(sample))
            else:
                if abs(energy - ground_energy) < 2:
                    # if classical gap is less than 2
                    self.assertTrue(csp.check(sample))
