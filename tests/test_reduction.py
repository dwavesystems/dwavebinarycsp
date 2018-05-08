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

import dwavebinarycsp


class TestDecomposition(unittest.TestCase):
    def test_irreducible_components(self):
        const = dwavebinarycsp.Constraint.from_configurations([(0, 0, 1), (1, 1, 1)], ['a', 'b', 'c'], dwavebinarycsp.BINARY)

        self.assertEqual(set(dwavebinarycsp.irreducible_components(const)), {('a', 'b'), ('c',)})

    def test_irreducible_components_one_fixed(self):
        const = dwavebinarycsp.Constraint.from_configurations(frozenset([(0, 1), (0, 0)]), ('a', 'b'), dwavebinarycsp.BINARY)

        self.assertEqual(set(dwavebinarycsp.irreducible_components(const)), {('a',), ('b',)})
