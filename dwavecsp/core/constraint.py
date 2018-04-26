"""
todo - describe Constraint
"""
import itertools

from collections import Sized, Callable

import dimod

from dwavecsp.exceptions import UnsatError

__all__ = ['Constraint']


class Constraint(Sized):
    """A constraint.

    Attributes:
        variables (tuple):
            The variables associated with the constraint.

        func (function):
            This function should return True for configurations of variables that satisfy the
            constraint. The inputs to the function are ordered by :attr:`~Constraint.variables`.

            Example:

                >>> const = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.BINARY)
                >>> const.func(0, 0)  # order matches variables
                True

        configurations (frozenset[tuple]):
            The valid configurations of the variables. Each configuration is a tuple of variable
            assignments ordered by :attr:`~Constraint.variables`.

            Example:

                >>> const = dwavecsp.Constraint.from_func(operator.ne, ['a', 'b'], dwavecsp.BINARY)
                >>> (0, 1) in const.configurations
                True
                >>> (1, 0) in const.configurations
                True

        vartype (:class:`dimod.Vartype`):
            The possible assignments for the constraint's variables.
            One of :attr:`~dimod.Vartype.SPIN` or :attr:`~dimod.Vartype.BINARY`. If the vartype is
            SPIN then the variables can be assigned -1 or 1, if BINARY then the variables can be
            assigned 0 or 1.

        name (str):
            The name of the constraint. If not provided on construction, will default to
            'Constraint'

            Example:
                >>> const = dwavecsp.Constraint.from_func(operator.ne, ['a', 'b'], dwavecsp.BINARY)
                >>> const.name
                'Constraint'
                >>> const = dwavecsp.Constraint.from_func(operator.ne, ['a', 'b'], dwavecsp.BINARY, name='neq')
                >>> const.name
                'neq'

    Several operations are also valid for constraints.

    Examples:
        Constraints have a length (the number of variables)

        >>> const = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.BINARY)
        >>> len(const)
        2

    """

    __slots__ = ('vartype', 'variables', 'configurations', 'func', 'name')

    #
    # Construction
    #

    @dimod.vartype_argument('vartype')
    def __init__(self, func, configurations, variables, vartype, name=None):

        self.vartype = vartype  # checked by decorator

        if not isinstance(func, Callable):
            raise TypeError("expected input 'func' to be callable")
        self.func = func

        self.variables = variables = tuple(variables)
        num_variables = len(variables)

        if not isinstance(configurations, frozenset):
            configurations = frozenset(tuple(config) for config in configurations)  # cast to tuples
        if len(configurations) == 0 and num_variables > 0:
            raise ValueError("constraint must have at least one feasible configuration")
        if not all(len(config) == num_variables for config in configurations):
            raise ValueError("all configurations should be of the same length")
        if len(vartype.value.union(*configurations)) >= 3:
            raise ValueError("configurations do not match vartype")
        self.configurations = configurations

        if name is None:
            name = 'Constraint'
        self.name = name

    @classmethod
    @dimod.vartype_argument('vartype')
    def from_func(cls, func, variables, vartype, name=None):
        """Construct a constraint from a validation function.

        Args:
            func (function):
                A function that evaluates true when the variables satisfy the constraint.

            variables (iterable):
                An iterable of variable labels.

            vartype (:class:`~dimod.Vartype`/str/set):
                Variable type for the binary quadratic model. Accepted input values:
                * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
                * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

            name (string, optional, default='Constraint'):
                Name for the constraint.

        Examples:

            Create a constraint that variables `a` and `b` are not equal.

            >>> const = dwavecsp.Constraint.from_func(operator.ne, ['a', 'b'], dwavecsp.BINARY)

        """
        variables = tuple(variables)

        configurations = frozenset(config
                                   for config in itertools.product(vartype.value, repeat=len(variables))
                                   if func(*config))

        return cls(func, configurations, variables, vartype, name)

    @classmethod
    def from_configurations(cls, configurations, variables, vartype, name=None):
        """Construct a constraint from a validation function.

        Args:
            configurations (iterable[tuple]):
                The valid configurations of the variables. Each configuration is a tuple of variable
                assignments ordered by :attr:`~Constraint.variables`.

            variables (iterable):
                An iterable of variable labels.

            vartype (:class:`~dimod.Vartype`/str/set):
                Variable type for the binary quadratic model. Accepted input values:
                * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
                * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

            name (string, optional, default='Constraint'):
                Name for the constraint.

        Examples:

            Create a constraint that variables `a` and `b` are not equal.

            >>> const = dwavecsp.Constraint.from_configurations([(0, 1), (1, 0)], ['a', 'b'], dwavecsp.BINARY)

        """
        def func(*args): return args in configurations

        return cls(func, configurations, variables, vartype, name)

    #
    # Special Methods
    #

    def __len__(self):
        """The number of variables."""
        return self.variables.__len__()

    def __repr__(self):
        return "Constraint.from_configurations({}, {}, {}, name='{}')".format(self.configurations,
                                                                              self.variables,
                                                                              self.vartype,
                                                                              self.name)

    def __eq__(self, constraint):
        return self.variables == constraint.variables and self.configurations == constraint.configurations

    def __ne__(self, constraint):
        return not self.__eq__(constraint)

    def __hash__(self):
        # uniquely defined by configurations/variables
        return hash((self.configurations, self.variables))

    def __or__(self, const):
        if not isinstance(const, Constraint):
            raise TypeError("unsupported operand type(s) for |: 'Constraint' and '{}'".format(type(const).__name__))

        if const and self and self.vartype is not const.vartype:
            raise ValueError("operand | only meaningful for Constraints with matching vartype")

        shared_variables = set(self.variables).intersection(const.variables)

        # dev note: if they share all variables, we could just act on the configurations

        if not shared_variables:
            # in this case we just append
            variables = self.variables + const.variables

            n = len(self)  # need to know how to divide up the variables

            def union(*args):
                return self.func(*args[:n]) or const.func(*args[n:])

            return self.from_func(union, variables, self.vartype, name='{} | {}'.format(self.name, const.name))

        variables = self.variables + tuple(v for v in const.variables if v not in shared_variables)

        def union(*args):
            solution = dict(zip(variables, args))
            return self.check(solution) or const.check(solution)

        return self.from_func(union, variables, self.vartype, name='{} | {}'.format(self.name, const.name))

    def __and__(self, const):
        if not isinstance(const, Constraint):
            raise TypeError("unsupported operand type(s) for &: 'Constraint' and '{}'".format(type(const).__name__))

        if const and self and self.vartype is not const.vartype:
            raise ValueError("operand & only meaningful for Constraints with matching vartype")

        shared_variables = set(self.variables).intersection(const.variables)

        # dev note: if they share all variables, we could just act on the configurations
        name = '{} & {}'.format(self.name, const.name)

        if not shared_variables:
            # in this case we just append
            variables = self.variables + const.variables

            n = len(self)  # need to know how to divide up the variables

            def intersection(*args):
                return self.func(*args[:n]) and const.func(*args[n:])

            return self.from_func(intersection, variables, self.vartype, name=name)

        variables = self.variables + tuple(v for v in const.variables if v not in shared_variables)

        def intersection(*args):
            solution = dict(zip(variables, args))
            return self.check(solution) and const.check(solution)

        return self.from_func(intersection, variables, self.vartype, name=name)

    #
    # verification
    #

    def check(self, solution):
        """Check that a solution satisfies the constraint.

        Args:
            solution (container):
                An assignment for the variables in the constraint.

        Returns:
            bool: True if the solution satisfies the constraint, else False.

        Examples:
            >>> const = dwavecsp.Constraint.from_configurations([(0, 1), (1, 0)], ['a', 'b'], dwavecsp.BINARY)
            >>> solution = {'a': 1, 'b': 1, 'c': 0}
            >>> const.check(solution)
            False
            >>> solution = {'a': 1, 'b': 0, 'c': 0}
            >>> const.check(solution)
            True

        """
        return self.func(*(solution[v] for v in self.variables))

    #
    # transformation
    #

    def fix_variable(self, v, value):
        """Fix the value of a variable and remove it from the constraint.

        Args:
            v (variable):
                A variable in the constraint to be fixed.

            val (int):
                Value assigned to the variable. Values must match the :class:`.Vartype` of the
                constraint.

        Examples:
            >>> const = dwavecsp.Constraint.from_func(operator.ne, ['a', 'b'], dwavecsp.BINARY)
            >>> const.fix_variable('a', 0)
            >>> const.check({'b': 1})
            True
            >>> const.check({'b': 0})
            False

        """
        variables = self.variables
        try:
            idx = variables.index(v)
        except ValueError:
            raise ValueError("given variable {} is not part of the constraint".format(v))

        if value not in self.vartype.value:
            raise ValueError("expected value to be in {}, received {} instead".format(self.vartype.value, value))

        configurations = frozenset(config[:idx] + config[idx + 1:]  # exclide the fixed var
                                   for config in self.configurations
                                   if config[idx] == value)

        if not configurations:
            raise UnsatError("fixing {} to {} makes this constraint unsatisfiable".format(v, value))

        variables = variables[:idx] + variables[idx + 1:]

        self.configurations = configurations
        self.variables = variables

        def func(*args): return args in configurations
        self.func = func

        self.name = '{} ({} fixed to {})'.format(self.name, v, value)

    def flip_variable(self, v):
        """Flip a variable in the constraint.

        Args:
            v (variable):
                A variable in the constraint to be flipped.

        Examples:
            >>> const = dwavecsp.Constraint.from_func(operator.eq, ['a', 'b'], dwavecsp.BINARY)
            >>> const.check({'a': 0, 'b': 0})
            True
            >>> const.flip_variable('a')
            >>> const.check({'a': 1, 'b': 0})
            True
            >>> const.check({'a': 0, 'b': 0})
            False

        """
        try:
            idx = self.variables.index(v)
        except ValueError:
            raise ValueError("variable {} is not a variable in constraint {}".format(v, self.name))

        if self.vartype is dimod.BINARY:

            original_func = self.func

            def func(*args):
                new_args = list(args)
                new_args[idx] = 1 - new_args[idx]  # negate v
                return original_func(*new_args)

            self.func = func

            self.configurations = frozenset(config[:idx] + (1 - config[idx],) + config[idx + 1:]
                                            for config in self.configurations)

        else:  # SPIN

            original_func = self.func

            def func(*args):
                new_args = list(args)
                new_args[idx] = -new_args[idx]  # negate v
                return original_func(*new_args)

            self.func = func

            self.configurations = frozenset(config[:idx] + (-config[idx],) + config[idx + 1:]
                                            for config in self.configurations)

        self.name = '{} ({} flipped)'.format(self.name, v)

    #
    # copy
    #

    def copy(self):
        """Create a copy."""
        # each object is itself immutable (except the function)
        return self.__class__(self.func, self.configurations, self.variables, self.vartype, name=self.name)
