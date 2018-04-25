import dimod

from dwavecsp.core.constraint import Constraint

__all__ = ['and_gate',
           'or_gate',
           'xor_gate',
           'halfadder_gate',
           'fulladder_gate']


@dimod.vartype_argument('vartype')
def and_gate(variables, vartype=dimod.BINARY, name='AND'):
    """AND gate."""

    variables = tuple(variables)

    if vartype is dimod.BINARY:
        configurations = frozenset([(0, 0, 0),
                                    (0, 1, 0),
                                    (1, 0, 0),
                                    (1, 1, 1)])

        def func(in1, in2, out): return (in1 and in2) == out

    else:
        # SPIN, vartype is checked by the decorator
        configurations = frozenset([(-1, -1, -1),
                                    (-1, +1, -1),
                                    (+1, -1, -1),
                                    (+1, +1, +1)])

        def func(in1, in2, out): return ((in1 > 0) and (in2 > 0)) == (out > 0)

    return Constraint(func, configurations, variables, vartype=vartype, name=name)


@dimod.vartype_argument('vartype')
def or_gate(variables, vartype=dimod.BINARY, name='OR'):
    """OR gate."""

    variables = tuple(variables)

    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0),
                             (0, 1, 1),
                             (1, 0, 1),
                             (1, 1, 1)])

        def func(in1, in2, out): return (in1 or in2) == out

    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1),
                             (-1, +1, +1),
                             (+1, -1, +1),
                             (+1, +1, +1)])

        def func(in1, in2, out): return ((in1 > 0) or (in2 > 0)) == (out > 0)

    return Constraint(func, configs, variables, vartype=vartype, name=name)


@dimod.vartype_argument('vartype')
def xor_gate(variables, vartype=dimod.BINARY, name='XOR'):
    """XOR constraint."""

    variables = tuple(variables)
    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0),
                             (0, 1, 1),
                             (1, 0, 1),
                             (1, 1, 0)])

        def func(in1, in2, out): return (in1 != in2) == out

    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1),
                             (-1, +1, +1),
                             (+1, -1, +1),
                             (+1, +1, -1)])

        def func(in1, in2, out): return ((in1 > 0) != (in2 > 0)) == (out > 0)

    return Constraint(func, configs, variables, vartype=vartype, name=name)


@dimod.vartype_argument('vartype')
def halfadder_gate(variables, vartype, name='HALF_ADDER'):
    """HALF_ADDER adder constraint."""

    variables = tuple(variables)

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

    def func(augend, addend, sum_, carry):
        total = (augend > 0) + (addend > 0)
        if total == 0:
            return (sum_ <= 0) and (carry <= 0)
        elif total == 1:
            return (sum_ > 0) and (carry <= 0)
        elif total == 2:
            return (sum_ <= 0) and (carry > 0)
        else:
            raise ValueError("func recieved unexpected values")

    return Constraint(func, configs, variables, vartype=vartype, name=name)


@dimod.vartype_argument('vartype')
def fulladder_gate(variables, vartype, name='FULL_ADDER'):
    """FULL_ADDER constraint."""

    variables = tuple(variables)

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

    def func(in1, in2, in3, sum_, carry):
        total = (in1 > 0) + (in2 > 0) + (in3 > 0)
        if total == 0:
            return (sum_ <= 0) and (carry <= 0)
        elif total == 1:
            return (sum_ > 0) and (carry <= 0)
        elif total == 2:
            return (sum_ <= 0) and (carry > 0)
        elif total == 3:
            return (sum_ > 0) and (carry > 0)
        else:
            raise ValueError("func recieved unexpected values")

    return Constraint(func, configs, variables, vartype=vartype, name=name)
