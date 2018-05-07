import unittest

import dwavebinarycsp


class TestDecomposition(unittest.TestCase):
    def test_irreducible_components(self):
        const = dwavebinarycsp.Constraint.from_configurations([(0, 0, 1), (1, 1, 1)], ['a', 'b', 'c'], dwavebinarycsp.BINARY)

        self.assertEqual(set(dwavebinarycsp.irreducible_components(const)), {('a', 'b'), ('c',)})

    def test_irreducible_components_one_fixed(self):
        const = dwavebinarycsp.Constraint.from_configurations(frozenset([(0, 1), (0, 0)]), ('a', 'b'), dwavebinarycsp.BINARY)

        self.assertEqual(set(dwavebinarycsp.irreducible_components(const)), {('a',), ('b',)})
