# Copyright 2018 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from itertools import combinations, count, product
import operator

import networkx as nx
import penaltymodel
import dimod

from dwavebinarycsp.core.constraint import Constraint
from dwavebinarycsp.exceptions import ImpossibleBQM
from dwavebinarycsp.reduction import irreducible_components
import dwavebinarycsp

__all__ = ['stitch']


def stitch(csp, min_classical_gap=2.0, max_graph_size=8):
    """Build a binary quadratic model with minimal energy levels at solutions to the specified constraint satisfaction
    problem.

    Args:
        csp (:obj:`.ConstraintSatisfactionProblem`):
            Constraint satisfaction problem.

        min_classical_gap (float, optional, default=2.0):
            Minimum energy gap from ground. Each constraint violated by the solution increases
            the energy level of the binary quadratic model by at least this much relative
            to ground energy.

        max_graph_size (int, optional, default=8):
            Maximum number of variables in the binary quadratic model that can be used to
            represent a single constraint.

    Returns:
        :class:`~dimod.BinaryQuadraticModel`

    Notes:
        For a `min_classical_gap` > 2 or constraints with more than two variables, requires
        access to factories from the penaltymodel_ ecosystem to construct the binary quadratic
        model.

    .. _penaltymodel: https://github.com/dwavesystems/penaltymodel

    Examples:
        This example creates a binary-valued constraint satisfaction problem
        with two constraints, :math:`a = b` and :math:`b \\ne c`, and builds
        a binary quadratic model such that
        each constraint violation by a solution adds the default minimum energy gap.

        >>> import operator
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> bqm = dwavebinarycsp.stitch(csp)

        Variable assignments that satisfy the CSP above, violate one, then two constraints,
        produce energy increases of the default minimum classical gap:

        >>> bqm.energy({'a': 0, 'b': 0, 'c': 1})  # doctest: +SKIP
        -2.0
        >>> bqm.energy({'a': 0, 'b': 0, 'c': 0})  # doctest: +SKIP
        0.0
        >>> bqm.energy({'a': 1, 'b': 0, 'c': 0}) #  doctest: +SKIP
        2.0

        This example creates a binary-valued constraint satisfaction problem
        with two constraints, :math:`a = b` and :math:`b \\ne c`, and builds
        a binary quadratic model with a minimum energy gap of 4.
        Note that in this case the conversion to binary quadratic model adds two
        ancillary variables that must be minimized over when solving.

        >>> import operator
        >>> import itertools
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> bqm = dwavebinarycsp.stitch(csp, min_classical_gap=4.0)
        >>> list(bqm)   # doctest: +SKIP
        ['a', 'aux1', 'aux0', 'b', 'c']

        Variable assignments that satisfy the CSP above, violate one, then two constraints,
        produce energy increases of the specified minimum classical gap:

        >>> min([bqm.energy({'a': 0, 'b': 0, 'c': 1, 'aux0': aux0, 'aux1': aux1}) for
        ... aux0, aux1 in list(itertools.product([0, 1], repeat=2))])  # doctest: +SKIP
        -6.0
        >>> min([bqm.energy({'a': 0, 'b': 0, 'c': 0, 'aux0': aux0, 'aux1': aux1}) for
        ... aux0, aux1 in list(itertools.product([0, 1], repeat=2))])  # doctest: +SKIP
        -2.0
        >>> min([bqm.energy({'a': 1, 'b': 0, 'c': 0, 'aux0': aux0, 'aux1': aux1}) for
        ... aux0, aux1 in list(itertools.product([0, 1], repeat=2))])  # doctest: +SKIP
        2.0

        This example finds for the previous example the minimum graph size.

        >>> import operator
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> for n in range(8, 1, -1):
        ...     try:
        ...         bqm = dwavebinarycsp.stitch(csp, min_classical_gap=4.0, max_graph_size=n)
        ...     except dwavebinarycsp.exceptions.ImpossibleBQM:
        ...         print(n+1)
        ...
        3

    """

    def aux_factory():
        for i in count():
            yield 'aux{}'.format(i)

    aux = aux_factory()

    bqm = dimod.BinaryQuadraticModel.empty(csp.vartype)

    # developer note: we could cache them and relabel, for now though let's do the simple thing
    # penalty_models = {}
    for const in csp.constraints:
        configurations = const.configurations

        if len(const.variables) > max_graph_size:
            msg = ("The given csp contains a constraint {const} with {num_var} variables. "
                   "This cannot be mapped to a graph with {max_graph_size} nodes. "
                   "Consider checking whether your constraint is irreducible."
                   "").format(const=const, num_var=len(const.variables), max_graph_size=max_graph_size)
            raise ImpossibleBQM(msg)

        pmodel = None

        if len(const) == 0:
            # empty constraint
            continue

        # at the moment, penaltymodel-cache cannot handle 1-variable PMs, so
        # we handle that case here
        if min_classical_gap <= 2.0 and len(const) == 1 and max_graph_size >= 1:
            bqm.update(_bqm_from_1sat(const))
            continue

        # turn the configurations into a sampleset
        samples_like = (list(configurations), const.variables)

        for G in iter_complete_graphs(const.variables, max_graph_size + 1, aux):

            try:
                pmodel, classical_gap = penaltymodel.get_penalty_model(
                    samples_like,
                    G,
                    min_classical_gap=min_classical_gap
                    )
            except penaltymodel.ImpossiblePenaltyModel:
                # not able to be built on this graph
                continue

            pmodel.change_vartype(csp.vartype, inplace=True)

            if classical_gap >= min_classical_gap:
                break

        else:
            msg = ("No penalty model can be built for constraint {}".format(const))
            raise ImpossibleBQM(msg)

        bqm.update(pmodel)

    return bqm


def _bqm_from_1sat(constraint):
    """create a bqm for a constraint with only one variable

    bqm will have exactly classical gap 2.
    """
    configurations = constraint.configurations
    num_configurations = len(configurations)

    bqm = dimod.BinaryQuadraticModel.empty(dimod.SPIN)

    if num_configurations == 1:
        val, = next(iter(configurations))
        v, = constraint.variables
        bqm.add_variable(v, -1 if val > 0 else +1)
    else:
        bqm.add_variables_from((v, 0.0) for v in constraint.variables)

    return bqm.change_vartype(constraint.vartype)


@nx.utils.nodes_or_number(0)
def iter_complete_graphs(start, stop, factory=None):
    """Iterate over complete graphs.

    Args:
        start (int/iterable):
            Define the size of the starting graph.
            If an int, the nodes will be index-labeled, otherwise should be an iterable of node
            labels.

        stop (int):
            Stops yielding graphs when the size equals stop.

        factory (iterator, optional):
            If provided, nodes added will be labeled according to the values returned by factory.
            Otherwise the extra nodes will be index-labeled.

    Yields:
        :class:`nx.Graph`

    """
    _, nodes = start
    nodes = list(nodes)  # we'll be appending

    if factory is None:
        factory = count()

    while len(nodes) < stop:
        # we need to construct a new graph each time, this is actually faster than copy and add
        # the new edges in any case
        G = nx.complete_graph(nodes)
        yield G

        v = next(factory)
        while v in G:
            v = next(factory)

        nodes.append(v)
