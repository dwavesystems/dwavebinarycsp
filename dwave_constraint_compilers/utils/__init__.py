from __future__ import division

import sys

from penaltymodel import SPIN, BINARY

__all__ = ['constraint_vartype', 'convert_constraint', 'sample_vartype', 'convert_sample', 'itervalues', 'iteritems']

_PY2 = sys.version_info.major == 2

if _PY2:
    range = xrange

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

else:

    def iteritems(d):
        return d.items()

    def itervalues(d):
        return d.values()


def constraint_vartype(constraint):
    for feasible_configuration in constraint['feasible_configurations']:
        i = 0
        while feasible_configuration[0] == 1 and i < len(feasible_configuration):
            i += 1

        if feasible_configuration[0] != 1:
            if feasible_configuration[0] in SPIN.value:
                return SPIN
            else:
                return BINARY

    # if we're here, either there are no feasible_configurations, every value in each configuration is 1.
    # either way, we can return pm.SPIN.
    return SPIN


def sample_vartype(sample):
    for assignment in itervalues(sample):
        if assignment != 1:
            if assignment in SPIN.value:
                return SPIN
            else:
                return BINARY

    # if we're here, either sample is empty, or every value is 1. Either way, we can return SPIN
    return SPIN


def convert_constraint(constraint, vartype=SPIN):
    spin_configurations = []

    if vartype == SPIN:
        def convert(i):
            return 2 * i - 1
    else:
        def convert(i):
            return (i + 1) // 2

    for feasible_configuration in constraint['feasible_configurations']:
        spin_configurations.append(tuple(map(convert, feasible_configuration)))

    constraint['feasible_configurations'] = spin_configurations
    return constraint


def convert_sample(sample, vartype=SPIN):
    if vartype == SPIN:
        def convert(i):
            return 2 * i - 1
    else:
        def convert(i):
            return (i + 1) // 2

    for var_name, assignment in iteritems(sample):
        sample[var_name] = convert(assignment)

    return sample

