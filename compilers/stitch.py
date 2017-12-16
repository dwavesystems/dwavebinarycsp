from __future__ import absolute_import

import sys
from itertools import combinations

import networkx as nx
import penaltymodel as pm

from compilers.constraint_specification_languages.internal import validate

__all__ = ['stitch']


_PY2 = sys.version_info.major == 2

if _PY2:
    range = xrange

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

else:

    def iteritems(d):
        return d.items()

    def itervalues(d):
        return d.values()


def stitch(constraints, do_validation=True):
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
        constraints (dict[str, dict]): A set of constraints conforming to the schema defined in the
                                      `constraint_specification_language`
        do_validation (bool): whether to validate the constraints using the JSON schema.

    Returns:
        :class:`pm.BinaryQuadraticModel`: The resulting :class:`BinaryQuadraticModel`.

    """
    if do_validation:
        validate(constraints)

    widgets = make_widgets_from(constraints)
    linear = {}
    quadratic = {}
    offset = 0
    for widget in widgets:
        for variable, bias in iteritems(widget.model.linear):
            linear[variable] = linear.get(variable, 0) + bias

        for relation, bias in iteritems(widget.model.quadratic):
            quadratic[relation] = quadratic.get(relation, 0) + bias

        offset += widget.model.offset

    return pm.BinaryQuadraticModel(linear, quadratic, offset, pm.SPIN)


def make_widgets_from(constraints):
    """
    Iterate through constraints and create :class:`PenaltyModel` widgets.

    Returns:
        list[:class:`pm.PenaltyModel`]: A list of :class:`pm.PenaltyModel` widgets representing the constraints.

    Raises:
        RuntimeError: If a :class:`PenaltyModel` cannot be found to represent the constraint.

    """
    max_graph_size = 8
    widgets = []
    for constraint in itervalues(constraints):
        if _constraint_vartype(constraint) != pm.SPIN:
            constraint = _convert_to_spin(constraint)
        widget = None
        n = len(constraint['variables'])
        while widget is None and n < max_graph_size:

            graph = make_complete_graph_from(constraint['variables'], n)

            spec = pm.Specification(
                graph=graph, decision_variables=constraint['variables'],
                feasible_configurations=constraint['feasible_configurations'],
                vartype=pm.SPIN
            )
            try:
                widget = pm.get_penalty_model(spec)
            except pm.ImpossiblePenaltyModel:
                pass
            n += 1

        if widget is not None:
            widgets.append(widget)
        else:
            raise RuntimeError('Cannot find penalty model for constraint: {}'.format(constraint))

    return widgets


def make_complete_graph_from(named_nodes, n):
    """
    Create a complete graph of size `n` and name the first `len(named_nodes)` using the values in named_nodes.

    Args:
        named_nodes (iterable): Iterable of node labels.
        n (int): The total number of nodes in the graph. Must be at least `len(named_nodes)`

    Returns:
        :class:`nx.Graph`: a complete graph.

    Raises:
        RuntimeError: if the `n` < len(named_nodes)

    """
    if n < len(named_nodes):
        raise RuntimeError('Graph must have at least {} nodes'.format(len(named_nodes)))

    # copy named_nodes so we don't modify the original input.
    all_nodes = named_nodes[:]

    if n > len(named_nodes):
        all_nodes.extend(range(len(named_nodes), n))

    graph = nx.Graph()
    graph.add_edges_from(combinations(all_nodes, 2))
    return graph


def _constraint_vartype(constraint):
    for feasible_configuration in constraint['feasible_configurations']:
        i = 0
        while feasible_configuration[0] == 1 and i < len(feasible_configuration):
            i += 1

        if feasible_configuration[0] != 1:
            if feasible_configuration[0] in pm.SPIN.value:
                return pm.SPIN
            else:
                return pm.BINARY

    # if we're here, either there are no feasible_configurations, every value in each configuration is 1.
    # either way, we can return pm.SPIN.
    return pm.SPIN


def _convert_to_spin(constraint):
    spin_configurations = []

    def to_spin(i):
        return 2 * i - 1

    for feasible_configuration in constraint['feasible_configurations']:
        spin_configurations.append(tuple(map(to_spin, feasible_configuration)))

    constraint['feasible_configurations'] = spin_configurations
    return constraint
