import itertools

from collections import Sized, Callable

import dimod

from dwavecsp.exceptions import UnsatError

__all__ = ['Constraint']


class Constraint(Sized):
    """tell folks to use from_*"""

    __slots__ = ('vartype', 'variables', 'configurations', 'func', 'name')

    #
    # Construction
    #

    @dimod.vartype_argument('vartype')
    def __init__(self, func, configurations, variables, vartype, name=None):

        self.vartype = vartype  # checked by decorator

        if not isinstance(func, Callable):
            raise TypeError("excpected input 'func' to be callable")
        self.func = func

        self.variables = variables = tuple(variables)
        num_variables = len(variables)

        if not isinstance(configurations, frozenset):
            configurations = frozenset(configurations)
        if not all(len(config) == num_variables for config in configurations):
            raise ValueError("all configurations should be of the same length")
        if len(vartype.value.union(*configurations)) > 3:
            raise ValueError("configurations do not match vartype")
        self.configurations = configurations

        if name is None:
            name = 'Constraint'
        self.name = name

    @classmethod
    @dimod.vartype_argument('vartype')
    def from_func(cls, func, variables, vartype, name=None):
        """todo"""
        configurations = frozenset(config
                                   for config in itertools.product(vartype.value, repeat=len(variables))
                                   if func(*config))

        return cls(func, configurations, variables, vartype, name)

    @classmethod
    def from_configurations(cls, configurations, variables, vartype, name='Constraint'):
        """todo"""
        def func(*args): return args in configurations

        return cls(func, configurations, variables, vartype, name)

    #
    # special methods
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
        """todo"""
        return self.func(*(solution[v] for v in self.variables))

    #
    # checking
    #

    def fix_variable(self, v, value):
        """Fix the value of a variable and remove it from the constraint.

        Args:
            v (variable):
                A variable in the constraint to be fixed.

            val (int):
                Value assigned to the variable. Values must match the :class:`.Vartype` of the
                constraint.

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
            raise UnsatError("fixing {} to {} makes this constraint unsatisfieable".format(v, value))

        variables = variables[:idx] + variables[idx + 1:]

        self.configurations = configurations
        self.variables = variables

        def func(*args): return args in configurations
        self.func = func

        self.name = '{} ({} fixed to {})'.format(self.name, v, value)
