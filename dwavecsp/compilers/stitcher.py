from itertools import combinations, count, product
import operator

from six import itervalues, iteritems

import networkx as nx
import penaltymodel as pm
import dimod

from dwavecsp.core.constraint import Constraint
from dwavecsp.reduction import irreducible_components

__all__ = ['stitch']


def stitch(csp, min_classical_gap=2.0, max_graph_size=8):
    """Build a binary quadratic model such that a solution that satisfies the constraint satisfaction
    problem minimizes the energy of the binary quadratic model.

    Args:
        csp (:obj:`.ConstraintSatisfactionProblem`):
            A constraint satisfaction problem.

        min_classical_gap (float, optional, default=2.0):
            Minimum energy gap allowed for each constraint. That is any solution that
            violates the constraint should have an energy in the bqm greater than ground + 2.

        max_graph_size (int, optional, default=8):
            Maximum number of variable in the bqm that can be used to represent a single
            constraint.

    Returns:
        :class:`~dimod.BinaryQuadraticModel`

    Notes:
        Requires access to factories from the penaltymodel_ ecosystem to construct the binary quadratic
        models for each constrain with more than two variables or for a min_classical_gap > 2.

    .. _penaltymodel: https://github.com/dwavesystems/penaltymodel

    Examples:

        >>> csp = dwavecsp.ConstraintSatisfactionProblem(dwavecsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> bqm = dwavecsp.stitch(csp)
        >>> bqm.energy({'a': 0, 'b': 0, 'c': 1})  # satisfies csp
        -2.0
        >>> bqm.energy({'a': 0, 'b': 0, 'c': 0})  # does not satisfy csp
        0.0

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

        if len(const) == 0:
            # empty constraint
            continue

        if min_classical_gap <= 2.0:
            if len(const) == 1:
                bqm.update(_bqm_from_1sat(const))
                continue
            elif len(const) == 2:
                bqm.update(_bqm_from_2sat(const))
                continue

        # developer note: we could cache them and relabel, for now though let's do the simple thing
        # if configurations in penalty_models:
        #     raise NotImplementedError

        for G in iter_complete_graphs(const.variables, max_graph_size, aux):
            spec = pm.Specification(
                graph=G,
                decision_variables=const.variables,
                feasible_configurations=configurations,
                vartype=csp.vartype
            )
            try:
                pmodel = pm.get_penalty_model(spec)
            except pm.ImpossiblePenaltyModel:
                pass

            if pmodel is None:
                raise RuntimeError("cannot build a penalty model")

            if pmodel.classical_gap >= min_classical_gap:
                break

        # developer note: we could cache them and relabel, for now though let's do the simple thing
        # penalty_models[configurations] = pmodel

        bqm.update(pmodel.model)

    return bqm


def _bqm_from_1sat(constraint):
    """create a bqm for a constraint with only one variable

    bqm will have exactly classical gap 2.
    """
    configurations = constraint.configurations
    num_configurations = len(configurations)

    bqm = dimod.BinaryQuadraticModel.empty(constraint.vartype)

    if num_configurations == 1:
        val, = next(iter(configurations))
        v, = constraint.variables
        bqm.add_variable(v, -1 if val > 0 else +1, vartype=dimod.SPIN)
    else:
        bqm.add_variables_from((v, 0.0) for v in constraint.variables)

    return bqm


def _bqm_from_2sat(constraint):
    """create a bqm for a constraint with two variables.

    bqm will have exactly classical gap 2.
    """
    configurations = constraint.configurations
    variables = constraint.variables
    vartype = constraint.vartype
    u, v = constraint.variables

    # if all configurations are present, then nothing is infeasible and the bqm is just all
    # 0.0s
    if len(configurations) == 4:
        return dimod.BinaryQuadraticModel.empty(constraint.vartype)

    # check if the constraint is irreducible, and if so, build the bqm for its two
    # components
    components = irreducible_components(constraint)
    if len(components) > 1:
        const0 = Constraint.from_configurations(((config[0],) for config in configurations),
                                                (u,), vartype)
        const1 = Constraint.from_configurations(((config[1],) for config in configurations),
                                                (v,), vartype)
        bqm = _bqm_from_1sat(const0)
        bqm.update(_bqm_from_1sat(const1))
        return bqm

    assert len(configurations) > 1, "single configurations should be irreducible"

    # if it is not irreducible, and there are infeasible configurations, then it is time to
    # start building a bqm
    bqm = dimod.BinaryQuadraticModel.empty(vartype)

    # if the constraint is not irreducible and has two configurations, then it is either eq or ne
    if all(operator.eq(*config) for config in configurations):
        bqm.add_interaction(u, v, -1, vartype=dimod.SPIN)  # equality
    elif all(operator.ne(*config) for config in configurations):
        bqm.add_interaction(u, v, +1, vartype=dimod.SPIN)  # inequality
    elif (1, 1) not in configurations:
        bqm.add_interaction(u, v, 2, vartype=dimod.BINARY)  # penalize (1, 1)
    elif (-1, +1) not in configurations and (0, 1) not in configurations:
        bqm.add_interaction(u, v, -2, vartype=dimod.BINARY)
        bqm.add_variable(v, 2, vartype=dimod.BINARY)
    elif (+1, -1) not in configurations and (1, 0) not in configurations:
        bqm.add_interaction(u, v, -2, vartype=dimod.BINARY)
        bqm.add_variable(u, 2, vartype=dimod.BINARY)
    else:
        # (0, 0) not in configurations
        bqm.add_interaction(u, v, 2, vartype=dimod.BINARY)
        bqm.add_variable(u, -2, vartype=dimod.BINARY)
        bqm.add_variable(v, -2, vartype=dimod.BINARY)

    return bqm


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
