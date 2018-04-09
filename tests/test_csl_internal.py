import unittest
from dwave_constraint_compilers.constraint_specification_languages.internal import validate
from jsonschema import ValidationError


class TestInternalLanguage(unittest.TestCase):

    def _test_exception_message(self, constraints, expected_message):
        with self.assertRaises(ValidationError) as expected:
            validate(constraints)

    def test_bad_constraint_wrong_constraint_type(self):

        bad_instance = {
            'all_variables': ['a', 'b'],
            'bad_constraint': []
        }

        self._test_exception_message(bad_instance, "[] is not of type 'object'")

    def test_bad_constraint_wrong_feasibles(self):
        constraints = {
            "1": {
                'feasible_configurations': [1],
                'variables': ['a', 'b', 'c']
            }
        }

        self._test_exception_message(constraints, "1 is not of type 'array'")

        constraints["1"]['feasible_configurations'] = ['a']
        self._test_exception_message(constraints, "'a' is not of type 'array'")

        constraints["1"]['feasible_configurations'] = [['a']]
        self._test_exception_message(constraints, "'a' is not of type 'number'")

    def test_constraint_with_tuples(self):
        constraints = {
            '1': {
                'feasible_configurations': [(0, 0, 0)],
                'variables': ['a', 'b', 'c']
            }
        }

        self.assertIsNone(validate(constraints))


if __name__ == '__main__':
    unittest.main()
