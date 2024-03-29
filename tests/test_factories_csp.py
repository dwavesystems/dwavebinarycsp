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

import unittest

import dwavebinarycsp.factories.csp as problem

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
