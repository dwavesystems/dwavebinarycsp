"""
The main functions for D-Wave Constraint Compilers.
"""
from __future__ import absolute_import

from dwave_constraint_compilers.compilers import stitch
from dwave_constraint_compilers.constraint_specification_languages.internal import validate
from dwave_constraint_compilers.utils import constraint_vartype, sample_vartype, convert_sample, iteritems

__all__ = ['satisfy', 'is_satisfied', 'iter_unsatisfied_constraints']


def satisfy(constraints, sampler, compilation_method=stitch, validate_constraints=True, **sampler_args):
    """Uses the provided sampler to try to satisfy the given constraints.

    Args:
        constraints (dict[str, dict]): A set of constraints conforming to the schema defined in the
            `constraint_specification_language`.

        sampler (object):
            A binary quadratic model sampler. A sampler is a process that
            samples from low energy states in models defined by an Ising
            equation or a Quadratic Unconstrained Binary Optimization Problem
            (QUBO). A sampler is expected to have a ‘sample_qubo’ and
            ‘sample_ising’ method. A sampler is expected to return an
            iterable of samples, in order of increasing energy.

        compilation_method (function, optional, default=:func:`.stitch`):
            A constraint compiler.

        validate_constraints (bool, optional, default=True):
             If True, validate that the constraints conform to the constrains JSON schema.

        **sampler_args: Additional keyword parameters are passed to the sampler.

    Returns:
        dict: A dict mapping each variable in the constraints to an assignment.
        The type of the assignment will match the inputs.

    Examples:
        >>> import dimod
        >>> constraints = {
        ...     'EQ1': {
        ...         'feasible_configurations': [(0, 0), (1, 1)],
        ...         'variables': ['a', 'b']},
        ...     'EQ2': {
        ...         'feasible_configurations': [(0, 0), (1, 1)],
        ...         'variables': ['c', 'b']},
        ...     'NEQ1': {
        ...         'feasible_configurations': [(0, 1), (1, 0)],
        ...         'variables': ['c', 'e']},
        ...     'NEQ2': {
        ...         'feasible_configurations': [(0, 1), (1, 0)],
        ...         'variables': ['a', 'e']}}
        >>> sampler = dimod.ExactSolver()
        >>> sample = dcc.satisfy(constraints, sampler)  # doctest: +SKIP
        >>> sample  # doctest: +SKIP
        {'a': 1, 'b': 1, 'c': 1, 'e': 0}

    """

    # check the the sampler is a dimod-compliant sampler
    # Author note: we want to handle samplers that have the same API as a dimod sampler but are not
    # themselves a subclass of the dimod TemplateSampler.
    if not hasattr(sampler, "sample_qubo") or not callable(sampler.sample_qubo):
        raise TypeError("expected sampler to have a 'sample_qubo' method")
    if not hasattr(sampler, "sample_ising") or not callable(sampler.sample_ising):
        raise TypeError("expected sampler to have a 'sample_ising' method")

    if validate_constraints:
        validate(constraints)

    # Figure out the Vartype now, in case the compilation method changes it. We'll need this to determine
    # what Vartype to return. For simplicity, let's assume the Vartype of the first constraint dictates
    # the Vartype for all of them.
    original_vartype = constraint_vartype(next(iter(constraints.values())))

    bqm = compilation_method(constraints)

    response = sampler.sample_ising(bqm.linear, bqm.quadratic, **sampler_args)

    # dimod samplers return dimod responses, which keep their samples sorted by increasing energy.
    # get the sample with lowest energy.
    sample = next(iter(response))

    if original_vartype != sample_vartype(sample):
        sample = convert_sample(sample, vartype=original_vartype)

    return sample


def is_satisfied(constraints, sample):
    """Determine if the sample satisfied the constraints.

    Args:
        constraints (dict[str, dict]): A set of constraints conforming to the schema defined in the
            `constraint_specification_language`.

        sample (dict[hashable, int]):
            A dict mapping each variable in the constraints to an assignment.

    Returns:
        bool: True if all if each constrain in constraints is met.

    Examples:
        >>> constraints = {
        ...     'EQ1': {
        ...         'feasible_configurations': [(0, 0), (1, 1)],
        ...         'variables': ['a', 'b']},
        ...     'EQ2': {
        ...         'feasible_configurations': [(0, 0), (1, 1)],
        ...         'variables': ['c', 'b']},
        ...     'NEQ1': {
        ...         'feasible_configurations': [(0, 1), (1, 0)],
        ...         'variables': ['c', 'e']},
        ...     'NEQ2': {
        ...         'feasible_configurations': [(0, 1), (1, 0)],
        ...         'variables': ['a', 'e']}}
        >>> sample = {'a': 1, 'b': 1, 'c': 1, 'e': 0}
        >>> dcc.is_satisfied(constraints, sample)
        True

    """
    return not any(iter_unsatisfied_constraints(constraints, sample))


def iter_unsatisfied_constraints(constraints, sample):
    """Determine which constraints are not satisfied by sample.

    Args:
        constraints (dict[str, dict]): A set of constraints conforming to the schema defined in the
            `constraint_specification_language`.

        sample (dict[hashable, int]):
            A dict mapping each variable in the constraints to an assignment.

    Returns:
        list: The names of the constraints in `constraints` that are not satisfied
        by sample.

    Examples:
        >>> constraints = {
        ...     'EQ1': {
        ...         'feasible_configurations': [(0, 0), (1, 1)],
        ...         'variables': ['a', 'b']},
        ...     'EQ2': {
        ...         'feasible_configurations': [(0, 0), (1, 1)],
        ...         'variables': ['c', 'b']},
        ...     'NEQ1': {
        ...         'feasible_configurations': [(0, 1), (1, 0)],
        ...         'variables': ['c', 'e']},
        ...     'NEQ2': {
        ...         'feasible_configurations': [(0, 1), (1, 0)],
        ...         'variables': ['a', 'e']}}
        >>> sample = {'a': 1, 'b': 1, 'c': 1, 'e': 1}
        >>> list(dcc.iter_unsatisfied_constraints(constraints, sample))  # doctest: +SKIP
        ['NEQ1', 'NEQ2']

    """
    for label, constraint in iteritems(constraints):
        config = tuple(sample[v] for v in constraint['variables'])
        if config not in constraint['feasible_configurations']:
            yield label
