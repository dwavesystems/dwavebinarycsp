"""Utility functions.

These are not meant to access directly. They are available by importing the
utils submodule.

>>> import dwave_constraint_compilers.utils as dccutils

"""
from __future__ import division

from six import iteritems, itervalues

from dimod import SPIN, BINARY

__all__ = ['constraint_vartype', 'convert_constraint', 'sample_vartype', 'convert_sample']


def constraint_vartype(constraint):
    """Determine the vartype of the given constraint.

    Args:
        constraint (dict):
            Must contain 'feasible_configurations' key.

    Returns:
        :class:`dimod.Vartype`: The type of the constraint, either :class:`dimod.Vartype.SPIN` or
        :class:`dimod.Vartype.BINARY`

    """
    seen_values = set().union(*constraint['feasible_configurations'])

    if seen_values.issubset(SPIN.value):
        return SPIN
    elif seen_values.issubset(BINARY.value):
        return BINARY

    raise ValueError("unknown constraint vartype")


def sample_vartype(sample):
    """Determine the vartype of the given sample.

    Args:
        sample (dict[hasable, int]): A single sample, as returned by :func:`.satisfy`.
            The keys should be the variables of a CSP, the values should be either
            in {-1, 1} or in {0, 1}.

    Returns:
        :class:`dimod.Vartype`: The type of the constraint, either :class:`dimod.Vartype.SPIN` or
        :class:`dimod.Vartype.BINARY`

    """
    seen_values = set(itervalues(sample))

    if seen_values.issubset(SPIN.value):
        return SPIN
    elif seen_values.issubset(BINARY.value):
        return BINARY

    raise ValueError("unknown constraint vartype")


def convert_constraint(constraint, vartype=SPIN):
    """Converts a constraint to the given vartype.

    Args:
        constraint (dict): Must contain 'feasible_configurations' key.

        vartype (:class:`penaltymodel.Vartype`, optional, default=:class:`penaltymodel.Vartype.SPIN`):
            The variable type to convert the constraint to.

    Returns:
        dict: The constraint, with the value of the 'feasible_configurations'
        modified to match the given vartype.

    Examples:
        >>> import penaltymodel as pm
        >>> constraint = {'feasible_configurations': [(0, 0), (1, 1)], 'variables': [0, 1]}
        >>> dcc.utils.convert_constraint(constraint, pm.SPIN)  # doctest: +SKIP
        {'feasible_configurations': [(-1, -1), (1, 1)], 'variables': [0, 1]}

    """
    spin_configurations = []

    if vartype == SPIN:
        def convert(i):
            return 2 * i - 1
    else:
        def convert(i):
            return (i + 1) // 2

    for feasible_configuration in constraint['feasible_configurations']:
        spin_configurations.append(tuple(map(convert, feasible_configuration)))

    constraint = constraint.copy()
    constraint['feasible_configurations'] = spin_configurations
    return constraint


def convert_sample(sample, vartype=SPIN):
    """Converts a sample to the given vartype.

    Args:
        sample (dict[hasable, int]): A single sample, as returned by :func:`.satisfy`.
            The keys should be the variables of a CSP, the values should be either
            in {-1, 1} or in {0, 1}.

        vartype (:class:`penaltymodel.Vartype`, optional, default=:class:`penaltymodel.Vartype.SPIN`):
            The variable type to convert the constraint to.

    Returns:
        dict: The sample, with the keys modified to match the new vartype.

    Examples:
        >>> import dimod
        >>> sample = {0: 0, 1: 1}
        >>> dcc.utils.convert_sample(sample, dimod.SPIN)
        {0: -1, 1: 1}

    """
    if vartype == SPIN:
        def convert(i):
            return 2 * i - 1
    else:
        def convert(i):
            return (i + 1) // 2

    new_sample = {}
    for var_name, assignment in iteritems(sample):
        new_sample[var_name] = convert(assignment)

    return new_sample
