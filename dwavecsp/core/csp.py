"""
todo - describe csp
"""
from collections import Callable, Iterable, defaultdict

import dimod

from dwavecsp.core.constraint import Constraint


class ConstraintSatisfactionProblem(object):
    """A constraint satisfaction problem.

    Args:
        vartype (:class:`~dimod.Vartype`/str/set):
            Variable type for the binary quadratic model. Accepted input values:

            * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
            * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

    Attributes:
        constraints (list[:obj:`.Constraint`]):
            The constraints that make up the constraint satisfaction problem. A valid solution
            will satisfy all of the constraints.

        variables (dict[variable, list[:obj:`.Constraint`]]):
            The keys are the variables in the constraint satisfaction problem. For each variable
            the value is a list of all of the Constraints associated with the variable.

        vartype (:class:`dimod.Vartype`):
            The possible assignments for the constraint satisfaction problem's variables.
            One of :attr:`~dimod.Vartype.SPIN` or :attr:`~dimod.Vartype.BINARY`. If the vartype is
            SPIN then the variables can be assigned -1 or 1, if BINARY then the variables can be
            assigned 0 or 1.


    """
    @dimod.vartype_argument('vartype')
    def __init__(self, vartype):
        self.vartype = vartype
        self.constraints = []
        self.variables = defaultdict(list)

    def __len__(self):
        return self.constraints.__len__()

    def add_constraint(self, constraint, variables=tuple()):
        """Add a constraint.

        Args:
            constraint (function/iterable/:obj:`.Constraint`):
                Add the constraint definition. See examples.

            variables(iterable):
                The variables associated with the constraint. Not required when `constraint` input
                is a :obj:`.Constraint`.

        Examples:

            There are three ways to add constraints.

            The first is to provide a function that evaluates True when the constraint is satisfied.
            The function should accept inputs (ordered by variables) of the type matching
            :attr:`~.ConstraintSatisfactionProblem.vartype`.

            >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.BINARY)
            >>> def all_equal(a, b, c):  # works for both dwavecsp.BINARY and dwavecsp.SPIN
            ...     return (a == b) and (b == c)
            >>> csp.add_constraint(all_equal, ['a', 'b', 'c'])
            >>> csp.check({'a': 0, 'b': 0, 'c': 0})
            True
            >>> csp.check({'a': 0, 'b': 0, 'c': 1})
            False

            The second is to explicitly specify the allowed configurations.

            >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.SPIN)
            >>> eq_configurations = {(-1, -1), (1, 1)}
            >>> csp.add_constraint(eq_configurations, ['v0', 'v1'])
            >>> csp.check({'v0': -1, 'v1': +1})
            False
            >>> csp.check({'v0': -1, 'v1': -1})
            True

            Finally the constraint can be an :obj:`.Constraint` - either one built explicitly
            or one built from one of the :mod:`dwavecsp.factories`.

            >>> import dwavecsp.factories.constraint.gates as gates
            >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.BINARY)
            >>> csp.add_constraint(gates.and_gate(['a', 'b', 'c']))  # add an AND gate
            >>> csp.add_constraint(gates.xor_gate(['a', 'c', 'd']))  # add an XOR gate
            >>> csp.check({'a': 1, 'b': 0, 'c': 0, 'd': 1})
            True

        """
        if isinstance(constraint, Constraint):
            if variables and (tuple(variables) != constraint.variables):
                raise ValueError("mismatched variables and Constraint")
        elif isinstance(constraint, Callable):
            constraint = Constraint.from_func(constraint, variables, self.vartype)
        elif isinstance(constraint, Iterable):
            constraint = Constraint.from_configurations(constraint, variables, self.vartype)
        else:
            raise TypeError("Unknown constraint type given")

        self.constraints.append(constraint)
        for v in constraint.variables:
            self.variables[v].append(constraint)

    def add_variable(self, v):
        """Add a variable.

        Args:
            v (variable):
                A variable in the constraint satisfaction problem. Can be of any type that
                can be a key of a dict.

        Examples:
            >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.SPIN)
            >>> csp.add_constraint(operator.eq, ['a', 'b'])
            >>> csp.add_variable('a')  # does nothing, already added as part of the constraint
            >>> csp.add_variable('c')
            >>> csp.check({'a': -1, 'b': -1, 'c': 1})
            True
            >>> csp.check({'a': -1, 'b': -1, 'c': -1})
            True

        """
        self.variables[v]  # because defaultdict will create it if it's not there

    def check(self, solution):
        """Check that a solution satisfies all of the constraints.

        Args:
            solution (container):
                An assignment for the variables in the constraint.

        Returns:
            bool: True if the solution satisfies all of the constraints, else False.

        Examples:
            >>> import dwavecsp.factories.constraint.gates as gates
            >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.BINARY)
            >>> csp.add_constraint(gates.and_gate(['a', 'b', 'c']))  # add an AND gate
            >>> csp.add_constraint(gates.xor_gate(['a', 'c', 'd']))  # add an XOR gate
            >>> csp.check({'a': 1, 'b': 0, 'c': 0, 'd': 1})
            True

        """
        return all(constraint.check(solution) for constraint in self.constraints)

    def fix_variable(self, v, value):
        """Fix the value of a variable and remove it from the constraint satisfaction problem.

        Args:
            v (variable):
                A variable in the constraint to be fixed.

            value (int):
                Value assigned to the variable. Values must match the :class:`.Vartype` of the
                constraint.

        Examples:
            >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.SPIN)
            >>> csp.add_constraint(operator.eq, ['a', 'b'])
            >>> csp.add_constraint(operator.ne, ['b', 'c'])
            >>> csp.check({'a': +1, 'b': +1, 'c': -1})
            True
            >>> csp.check({'a': -1, 'b': -1, 'c': +1})
            True
            >>> csp.fix_variable('b', +1)
            >>> csp.check({'a': +1, 'b': +1, 'c': -1})  # 'b' is ignored
            True
            >>> csp.check({'a': -1, 'b': -1, 'c': +1})
            False
            >>> csp.check({'a': +1, 'c': -1})
            True
            >>> csp.check({'a': -1, 'c': +1})
            False


        """
        if v not in self.variables:
            raise ValueError("given variable {} is not part of the constraint satisfaction problem".format(v))

        for constraint in self.variables[v]:
            constraint.fix_variable(v, value)

        del self.variables[v]  # delete the variable


CSP = ConstraintSatisfactionProblem
"""An alias for :class:`.ConstraintSatisfactionProblem`."""
