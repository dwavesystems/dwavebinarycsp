from pkg_resources import resource_filename
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
    with open(resource_filename(__name__, 'constraints_schema.json')) as schema_file:
        schema = json.load(schema_file)

    constraints = json.loads(json.dumps(constraints))

    json_validate(constraints, schema)
