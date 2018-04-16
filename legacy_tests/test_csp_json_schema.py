import unittest

from jsonschema import ValidationError

from dwave_constraint_compilers.io.json import validate_csp


class TestInternalLanguage(unittest.TestCase):
    def test_validate_csp_correct(self):
        csp = {"constraints": [{"feasible_configurations": [(-1, +1), (+1, -1)],
                                "variables": ['a', 'b'],
                                "name": 'NEQ'
                                }
                               ],
               "vartype": 'SPIN'}

        validate_csp(csp)


if __name__ == '__main__':
    unittest.main()
