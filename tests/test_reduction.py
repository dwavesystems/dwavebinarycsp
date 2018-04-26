import unittest

import dwavecsp


class TestDecomposition(unittest.TestCase):
    def test_irreducible_components(self):
        const = dwavecsp.Constraint.from_configurations([(0, 0, 1), (1, 1, 1)], ['a', 'b', 'c'], dwavecsp.BINARY)

        self.assertEqual(set(dwavecsp.irreducible_components(const)), {('a', 'b'), ('c',)})

    def test_irreducible_components_one_fixed(self):
        const = dwavecsp.Constraint.from_configurations(frozenset([(0, 1), (0, 0)]), ('a', 'b'), dwavecsp.BINARY)

        self.assertEqual(set(dwavecsp.irreducible_components(const)), {('a',), ('b',)})
