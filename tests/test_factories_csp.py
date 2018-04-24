import unittest

import dwavecsp.factories.csp as problem


class TestSAT(unittest.TestCase):
    def test_random_satisfiable_2in4sat(self):

        csp = problem.random_2in4sat(4, 1)
