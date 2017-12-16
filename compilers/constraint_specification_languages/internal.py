import os
import json
from jsonschema import validate as json_validate
from jsonschema import ValidationError

__all__ = ['validate']


def validate(constraints):
    """
    Validate that the constraints conform to the constrains JSON schema.

    Args:
        constraints (dict[str, dict]]): The constraints that require validation.

    Raises:
        ValidationError: An error if the instance violates the schema.
    """
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'constraints_schema.json')
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)

    constraints = json.loads(json.dumps(constraints))

    json_validate(constraints, schema)
