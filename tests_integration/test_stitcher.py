import unittest
import operator

import dimod

import dwavecsp

try:
    import penaltymodel_maxgap
    _maxgap = True
except ImportError:
    _maxgap = False


class TestStitch(unittest.TestCase):
    @unittest.skipUnless(_maxgap, 'needs penaltymodel-maxgap installed')
    def test_stitch_multiplication_circuit(self):

        circuit = dwavecsp.factories.multiplication_circuit(3)  # 3x3=6 bit

        # the circuit csp is too large for dimod's exact solver to solve quickly, so let's go ahead
        # and fix the inputs and outputs to ones that satisfy the csp and solve for the aux variables

        # 15 = 3 * 5

        fixed_variables = dict([('p0', 1), ('p1', 1), ('p2', 1), ('p3', 1), ('p4', 0), ('p5', 0),  # 15
                                ('a0', 1), ('a1', 1), ('a2', 0),  # 3
                                ('b0', 1), ('b1', 0), ('b2', 1)])  # 5

        for v, val in fixed_variables.items():
            circuit.fix_variable(v, val)

        # original circuit
        original_circuit = dwavecsp.factories.multiplication_circuit(3)

        # we are using an exact solver, so we only need a positive classical gap
        bqm = dwavecsp.stitch(circuit, min_classical_gap=.1)

        resp = dimod.ExactSolver().sample(bqm)

        ground_energy = min(resp.data_vectors['energy'])

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
