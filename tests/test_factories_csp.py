import unittest

import dwavecsp.factories.csp as problem

import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


class TestSAT(unittest.TestCase):
    def test_random_2in4sat(self):
        csp = problem.random_2in4sat(4, 1)

    def test_random_xorsat(self):
        csp = problem.random_xorsat(3, 1)


class TestCircuits(unittest.TestCase):
    def test_multiplication_circuit(self):
        csp = problem.multiplication_circuit(3)
        print()
        for const in csp.constraints:
            print(const.name)
