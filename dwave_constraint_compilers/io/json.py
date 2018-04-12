from __future__ import absolute_import

import json

from pkg_resources import resource_filename
from jsonschema import validate

with open(resource_filename(__name__, 'csp_schema.json'), 'r') as schema_file:
    csp_json_schema = json.load(schema_file)


def validate_csp(csp):
    """Validate the form on the constraint satisfaction problem.

    Args:
        csp (dict): The constraint statisfaction problem.

    Raises:
        :py:exc:`~jsonschema.ValidationError`: An error if the instance violates the schema.

    """

    # 'round' all of the python objects to their json equivalents, e.g. [(-1, 1)] -> [[-1, 1]]
    csp = json.loads(json.dumps(csp))

    validate(csp, csp_json_schema)
