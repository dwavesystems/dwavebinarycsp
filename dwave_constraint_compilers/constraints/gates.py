import dimod

__all__ = ['AND', 'OR', 'XOR', 'HALF_ADDER', 'FULL_ADDER']


@dimod.vartype_argument('vartype')
def AND(in1, in2, out, vartype=dimod.BINARY, name='AND'):
    """An AND constraint.

    """
    # configs are frozensets because they are unordered
    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0),
                             (0, 1, 0),
                             (1, 0, 0),
                             (1, 1, 1)])
    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1),
                             (-1, +1, -1),
                             (+1, -1, -1),
                             (+1, +1, +1)])

    # store variables in a tuple so users are not tempted to change them
    return {'feasible_configurations': configs,
            'name': name,
            'variables': (in1, in2, out)}


@dimod.vartype_argument('vartype')
def OR(in1, in2, out, vartype=dimod.BINARY, name='OR'):
    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0),
                             (0, 1, 1),
                             (1, 0, 1),
                             (1, 1, 1)])
    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1),
                             (-1, +1, +1),
                             (+1, -1, +1),
                             (+1, +1, +1)])

    # store variables in a tuple so users are not tempted to change them
    return {'feasible_configurations': configs,
            'name': name,
            'variables': (in1, in2, out)}


@dimod.vartype_argument('vartype')
def XOR(in1, in2, out, vartype=dimod.BINARY, name='XOR'):
    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0),
                             (0, 1, 1),
                             (1, 0, 1),
                             (1, 1, 0)])
    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1),
                             (-1, +1, +1),
                             (+1, -1, +1),
                             (+1, +1, -1)])

    # store variables in a tuple so users are not tempted to change them
    return {'feasible_configurations': configs,
            'name': name,
            'variables': (in1, in2, out)}


@dimod.vartype_argument('vartype')
def HALF_ADDER(augend, addend, sum_, carry, vartype=dimod.BINARY, name='HALF_ADDER'):
    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0, 0),
                             (0, 1, 1, 0),
                             (1, 0, 1, 0),
                             (1, 1, 0, 1)])
    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1, -1),
                             (-1, +1, +1, -1),
                             (+1, -1, +1, -1),
                             (+1, +1, -1, +1)])

    # store variables in a tuple so users are not tempted to change them
    return {'feasible_configurations': configs,
            'name': name,
            'variables': (augend, addend, sum_, carry)}


@dimod.vartype_argument('vartype')
def FULL_ADDER(augend, addend, summand, sum_, carry, vartype=dimod.BINARY, name='FULL_ADDER'):
    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0, 0, 0),
                             (0, 0, 1, 1, 0),
                             (0, 1, 0, 1, 0),
                             (0, 1, 1, 0, 1),
                             (1, 0, 0, 1, 0),
                             (1, 0, 1, 0, 1),
                             (1, 1, 0, 0, 1),
                             (1, 1, 1, 1, 1)])
    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1, -1, -1),
                             (-1, -1, +1, +1, -1),
                             (-1, +1, -1, +1, -1),
                             (-1, +1, +1, -1, +1),
                             (+1, -1, -1, +1, -1),
                             (+1, -1, +1, -1, +1),
                             (+1, +1, -1, -1, +1),
                             (+1, +1, +1, +1, +1)])

    # store variables in a tuple so users are not tempted to change them
    return {'feasible_configurations': configs,
            'name': name,
            'variables': (augend, addend, summand, sum_, carry)}
