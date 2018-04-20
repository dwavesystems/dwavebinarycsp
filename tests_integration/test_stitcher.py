import unittest
import operator

import dimod

import dwavecsp
from dwavecsp.compilers import stitcher


class TestStitch(unittest.TestCase):
    def test_stitch(self):

        csp = dwavecsp.CSP(dwavecsp.SPIN)

        csp.add_constraint(operator.eq, ['a', 'b'])
        csp.add_constraint(operator.ne, ['b', 'c'])
        csp.add_constraint(operator.eq, ['c', 'd'])

        bqm = dwavecsp.stitch(csp)

        response = dimod.ExactSolver().sample(bqm)

        ground_energy = min(en for en, in response.data(['energy']))

        for sample, energy in response.data(['sample', 'energy']):
            if energy == ground_energy:
                self.assertTrue(csp.check(sample))
            else:
                self.assertFalse(csp.check(sample))
