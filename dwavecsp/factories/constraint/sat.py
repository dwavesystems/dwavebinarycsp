import itertools

import dimod

from dwavecsp.core.constraint import Constraint

__all__ = ['sat2in4']


@dimod.vartype_argument('vartype')
def sat2in4(*args, vartype=dimod.BINARY, name='2-in-4', pos=tuple(), neg=tuple()):
    """2in4sat"""

    pos = args + tuple(pos)
    neg = tuple(neg)

    variables = pos + neg

    if len(variables) != 4:
        raise ValueError("")

    if neg and (len(neg) < 4):

        if vartype is dimod.BINARY:
            def iter_config():
                for u, v in itertools.combinations((0, 1, 2, 3), 2):
                    config = [0] * len(pos) + [1] * len(neg)
                    config[u] = 1 - config[u]
                    config[v] = 1 - config[v]

                    yield tuple(config)
            configurations = frozenset(iter_config())
        else:
            def iter_config():
                for u, v in itertools.combinations((0, 1, 2, 3), 2):
                    config = [-1] * len(pos) + [1] * len(neg)
                    config[u] *= -1
                    config[v] *= -1

                    yield tuple(config)
            configurations = frozenset(iter_config())

        return Constraint.from_configurations(configurations=configurations,
                                              variables=variables, vartype=vartype, name=name)
    else:
        # we can just construct them directly for speed
        if vartype is dimod.BINARY:
            configurations = frozenset([(0, 0, 1, 1),
                                        (0, 1, 0, 1),
                                        (1, 0, 0, 1),
                                        (0, 1, 1, 0),
                                        (1, 0, 1, 0),
                                        (1, 1, 0, 0)])
        else:
            # SPIN, vartype is checked by the decorator
            configurations = frozenset([(-1, -1, +1, +1),
                                        (-1, +1, -1, +1),
                                        (+1, -1, -1, +1),
                                        (-1, +1, +1, -1),
                                        (+1, -1, +1, -1),
                                        (+1, +1, -1, -1)])

        def func(a, b, c, d):
            if a == b:
                return (b != c) and (c == d)
            elif a == c:
                # a != b
                return b == d
            else:
                # a != b, a != c -> b == c
                return a == d

    return Constraint(func=func, configurations=configurations, variables=variables,
                      vartype=vartype, name=name)
