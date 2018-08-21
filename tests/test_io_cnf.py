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
import itertools
import unittest
import os.path as path

import dwavebinarycsp as dbcsp


class Test_cnf_to_csp(unittest.TestCase):
    def test_simple(self):
        cnf = ['c  simple_v3_c2.cnf',
               'c',
               'p cnf 3 2',
               '1 -3 0',
               '2 3 -1 0',
               ]

        csp = dbcsp.cnf.load_cnf(cnf)

        for config in itertools.product((0, 1), repeat=3):
            sample = dict(zip([1, 2, 3], config))

            if (sample[1] or 1 - sample[3]) and (sample[2] or sample[3] or 1 - sample[1]):
                self.assertTrue(csp.check(sample))
            else:
                self.assertFalse(csp.check(sample))

    def test_file0(self):
        filepath = path.join(path.dirname(path.abspath(__file__)), 'data', 'test0.cnf')
        with open(filepath, 'r') as fp:
            csp = dbcsp.cnf.load_cnf(fp)

        self.assertEqual(len(csp), 192)
        self.assertEqual(len(csp.variables), 17)

    def test_file1(self):
        filepath = path.join(path.dirname(path.abspath(__file__)), 'data', 'test1.cnf')
        with open(filepath, 'r') as fp:
            csp = dbcsp.cnf.load_cnf(fp)

        self.assertEqual(len(csp), 153)
        self.assertEqual(len(csp.variables), 98)
