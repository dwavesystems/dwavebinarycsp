import unittest

import dimod

import dwavecsp
import dwavecsp.testing as dcspt


class TestGates(unittest.TestCase):

    def test_AND(self):
        and_ = dwavecsp.and_gate(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

        and_ = dwavecsp.generators.and_gate(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

    def test_OR(self):
        or_ = dwavecsp.generators.or_gate(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

        or_ = dwavecsp.generators.or_gate(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

    def test_XOR(self):
        or_ = dwavecsp.generators.xor_gate(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

        or_ = dwavecsp.generators.xor_gate(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

    def test_HALF_ADDER(self):
        or_ = dwavecsp.generators.halfadder_gate(0, 1, 2, 3, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

        or_ = dwavecsp.generators.halfadder_gate(0, 1, 2, 3, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

    def test_FULL_ADDER(self):
        or_ = dwavecsp.generators.fulladder_gate(0, 1, 2, 'a', 'b', dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')

        or_ = dwavecsp.generators.fulladder_gate(0, 1, 2, 'a', 'b', dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')
