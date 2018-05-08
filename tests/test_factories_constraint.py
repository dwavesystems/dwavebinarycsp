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
import itertools

import dimod

import dwavebinarycsp
import dwavebinarycsp.testing as dcspt
import dwavebinarycsp.factories.constraint as constraint


class TestGates(unittest.TestCase):

    def test_AND(self):
        and_ = constraint.and_gate([0, 1, 2], vartype=dwavebinarycsp.BINARY)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

        and_ = constraint.and_gate([0, 1, 2], vartype=dwavebinarycsp.SPIN)
        dcspt.assert_consistent_constraint(and_)

        self.assertEqual(and_.name, 'AND')

    def test_OR(self):
        or_ = constraint.or_gate([0, 1, 2], vartype=dwavebinarycsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

        or_ = constraint.or_gate([0, 1, 2], vartype=dwavebinarycsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'OR')

    def test_XOR(self):
        or_ = constraint.xor_gate([0, 1, 2], vartype=dwavebinarycsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

        or_ = constraint.xor_gate([0, 1, 2], vartype=dwavebinarycsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'XOR')

    def test_HALF_ADDER(self):
        or_ = constraint.halfadder_gate([0, 1, 2, 3], vartype=dwavebinarycsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

        or_ = constraint.halfadder_gate([0, 1, 2, 3], vartype=dwavebinarycsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'HALF_ADDER')

    def test_FULL_ADDER(self):
        or_ = constraint.fulladder_gate([0, 1, 2, 'a', 'b'], vartype=dwavebinarycsp.BINARY)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')

        or_ = constraint.fulladder_gate([0, 1, 2, 'a', 'b'], vartype=dwavebinarycsp.SPIN)
        dcspt.assert_consistent_constraint(or_)

        self.assertEqual(or_.name, 'FULL_ADDER')


class TestSat(unittest.TestCase):
    def test_sat2in4(self):
        const = constraint.sat2in4(['a', 'b', 'c', 'd'])
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
