from collections import Callable, Iterable, defaultdict

import dimod

from dwavecsp.core.constraint import Constraint


class ConstraintSatisfactionProblem(object):
    @dimod.vartype_argument('vartype')
    def __init__(self, vartype):
        self.vartype = vartype
        self.constraints = []
        self.variables = defaultdict(list)

    def add_constraint(self, constraint, variables=tuple()):
        if isinstance(constraint, Constraint):
            pass
        elif isinstance(constraint, Callable):
            constraint = Constraint.from_func(constraint, variables, self.vartype)
        elif isinstance(constraint, Iterable):
            constraint = Constraint.from_configurations(constraint, variables, self.vartype)
        else:
            raise TypeError("Unknown constraint type given")

        self.constraints.append(constraint)
        for v in constraint.variables:
            self.variables[v].append(constraint)

    def check(self, solution):
        return all(constraint.check(solution) for constraint in self.constraints)

    def fix_variable(self, v, value):
        """todo"""
        if v not in self.variables:
            raise ValueError("given variable {} is not part of the constraint satisfaction problem".format(v))

        for constraint in self.variables[v]:
            constraint.fix_variable(v, value)

        del self.variables[v]  # delete the variable


CSP = ConstraintSatisfactionProblem
"""An alias for :class:`.ConstraintSatisfactionProblem`."""
