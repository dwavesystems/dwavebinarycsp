import unittest
import itertools

import dimod

import dwavecsp
import dwavecsp.testing as dcspt
import dwavecsp.factories.constraint as constraint


class TestGates(unittest.TestCase):

    def test_AND(self):
        and_ = constraint.and_gate(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

        and_ = constraint.and_gate(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

    def test_OR(self):
        or_ = constraint.or_gate(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

        or_ = constraint.or_gate(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

    def test_XOR(self):
        or_ = constraint.xor_gate(0, 1, 2, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

        or_ = constraint.xor_gate(0, 1, 2, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

    def test_HALF_ADDER(self):
        or_ = constraint.halfadder_gate(0, 1, 2, 3, dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

        or_ = constraint.halfadder_gate(0, 1, 2, 3, dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

    def test_FULL_ADDER(self):
        or_ = constraint.fulladder_gate(0, 1, 2, 'a', 'b', dwavecsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')

        or_ = constraint.fulladder_gate(0, 1, 2, 'a', 'b', dwavecsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')


class TestSat(unittest.TestCase):
    def test_sat2in4(self):
        const = constraint.sat2in4('a', 'b', 'c', 'd')
        dcspt.assert_consistent_constraint(const)

        valid = set()
        for u, v in itertools.combinations(range(4), 2):
            config = [0, 0, 0, 0]
            config[u], config[v] = 1, 1

            valid.add(tuple(config))

        for config in itertools.product([0, 1], repeat=4):
            if config in valid:
                self.assertTrue(const.func(*config))
            else:
                self.assertFalse(const.func(*config))

    def test_sat2in4_with_negation(self):
        const = constraint.sat2in4(pos=('a', 'd'), neg=('c', 'b'))
        dcspt.assert_consistent_constraint(const)

        self.assertTrue(const.check({'a': 1, 'b': 1, 'c': 1, 'd': 1}))
