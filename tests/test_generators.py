import unittest

import dimod

import dwavecsp
import dwavecsp.testing as dcspt


class TestGates(unittest.TestCase):

    def test_AND(self):
        and_ = dwavecsp.generators.AND(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

        and_ = dwavecsp.generators.AND(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

    def test_OR(self):
        or_ = dwavecsp.generators.OR(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

        or_ = dwavecsp.generators.OR(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

    def test_XOR(self):
        or_ = dwavecsp.generators.XOR(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

        or_ = dwavecsp.generators.XOR(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

    def test_HALF_ADDER(self):
        or_ = dwavecsp.generators.HALF_ADDER(0, 1, 2, 3, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

        or_ = dwavecsp.generators.HALF_ADDER(0, 1, 2, 3, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

    def test_FULL_ADDER(self):
        or_ = dwavecsp.generators.FULL_ADDER(0, 1, 2, 'a', 'b', dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')

        or_ = dwavecsp.generators.FULL_ADDER(0, 1, 2, 'a', 'b', dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')
