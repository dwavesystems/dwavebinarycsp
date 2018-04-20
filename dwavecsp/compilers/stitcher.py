from itertools import combinations, count

from six import itervalues, iteritems

import networkx as nx
import penaltymodel as pm
import dimod

__all__ = ['stitch']


def stitch(csp, min_classical_gap=2.0, max_graph_size=8):
    """
    Create :class:`pm.PenaltyModel` widgets from the constraints given, and 'stitch' them together:
    The variable set of the new model is the additive union of the variable sets of the widgets,
    the relations set of the new model is the additive union of the relation sets of the widgets.

    That is, the new widget contains every variable and coupler that is in any widget,
    and the bias of a variable or relation is the sum of the biases in of the variable
    or relation in all widgets that contain it.

    Similarly, the offset is summed across all widgets.

    All constraints are converted to :class:`pm.Vartype.SPIN`.

    Args:
        csp (:obj:`.ConstraintSatisfactionProblem`):
            todo

        min_classical_gap (float):
            todo

        max_graph_size (int):
            todo

    Returns:
        :class:`~dimod.BinaryQuadraticModel`

    """
    def aux_factory():
        for i in itertools.count():
            yield 'aux{}'.format(i)

    aux = aux_factory()

    bqm = dimod.BinaryQuadraticModel.empty(csp.vartype)

    # developer note: we could cache them and relabel, for now though let's do the simple thing
    # penalty_models = {}
    for const in csp.constraints:
        configurations = const.configurations

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
