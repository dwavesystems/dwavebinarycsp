import dimod

from dwavecsp.core.constraint import Constraint

__all__ = ['and_gate', 'or_gate', 'xor_gate', 'halfadder_gate', 'fulladder_gate']


class and_gate(Constraint):
    """AND constraint."""
    __slots__ = ()

    @dimod.vartype_argument('vartype')
    def __init__(self, in1, in2, out, vartype, name='AND'):

        self.name = name
        self.vartype = vartype
        self.variables = (in1, in2, out)

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

        self.configurations = configurations
        self.func = func


class or_gate(Constraint):
    """OR constraint."""
    __slots__ = ()

    @dimod.vartype_argument('vartype')
    def __init__(self, in1, in2, out, vartype, name='OR'):

        self.name = name
        self.vartype = vartype
        self.variables = (in1, in2, out)

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

        self.configurations = configs
        self.func = func


class xor_gate(Constraint):
    """XOR constraint."""
    __slots__ = ()

    @dimod.vartype_argument('vartype')
    def __init__(self, in1, in2, out, vartype, name='XOR'):

        self.name = name
        self.vartype = vartype
        self.variables = (in1, in2, out)

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

        self.configurations = configs
        self.func = func


class halfadder_gate(Constraint):
    """HALF_ADDER adder constraint."""
    __slots__ = ()

    @dimod.vartype_argument('vartype')
    def __init__(self, augend, addend, sum_, carry, vartype, name='HALF_ADDER'):

        self.name = name
        self.vartype = vartype
        self.variables = (augend, addend, sum_, carry)

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

        self.configurations = configs
        self.func = func


class fulladder_gate(Constraint):
    """FULL_ADDER constraint."""
    __slots__ = ()

    @dimod.vartype_argument('vartype')
    def __init__(self, in1, in2, in3, sum_, carry, vartype, name='FULL_ADDER'):

        self.name = name
        self.vartype = vartype
        self.variables = (in1, in2, in3, sum_, carry)

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

        self.configurations = configs
        self.func = func
