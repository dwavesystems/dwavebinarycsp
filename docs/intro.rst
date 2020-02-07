.. _intro_csp:

============
Introduction
============

`dwavebinarycsp` is a library to construct a binary quadratic :term:`model` from a constraint
satisfaction problem (CSP) with small constraints over binary variables (represented
as either binary values {0, 1} or spin values {-1, 1}).

Constraint Satisfaction Problems
================================

Constraint satisfaction problems require that all a problem's variables be assigned
values, out of a finite domain, that result in the satisfying of all constraints.

The map-coloring CSP, for example, is to assign a color to each region of a map such that
any two regions sharing a border have different colors.

.. figure:: _images/Problem_MapColoring.png
   :name: Problem_MapColoring
   :alt: image
   :align: center
   :scale: 70 %

   Coloring a map of Canada with four colors.

The constraints for the map-coloring problem can be expressed as follows:

* Each region is assigned one color only, of :math:`C` possible colors.
* The color assigned to one region cannot be assigned to adjacent regions.

Binary Constraint Satisfaction Problems
=======================================

Solving such problems as the map-coloring CSP on a :term:`sampler` such as the
D-Wave system necessitates that the
mathematical formulation use binary variables because the solution is implemented physically
with qubits, and so must translate to spins :math:`s_i\in\{-1,+1\}` or equivalent binary
values :math:`x_i\in \{0,1\}`. This means that in formulating the problem
by stating it mathematically, you might use unary encoding to represent the :math:`C` colors:
each region is represented by :math:`C` variables, one for each possible color, which
is set to value :math:`1` if selected, while the remaining :math:`C-1` variables are
:math:`0`.

Another example is logical circuits. Logic gates such as AND, OR, NOT, XOR etc
can be viewed as binary CSPs: the mathematically expressed relationships between binary inputs
and outputs must meet certain validity conditions. For inputs :math:`x_1,x_2` and
output :math:`y` of an AND gate, for example, the constraint to satisfy, :math:`y=x_1x_2`,
can be expressed as a set of valid configurations: (0, 0, 0), (0, 1, 0), (1, 0, 0),
(1, 1, 1), where the variable order is :math:`(x_1, x_2, y)`.

.. table:: Boolean AND Operation
   :name: BooleanANDAsPenalty

   ===============  ============================
   :math:`x_1,x_2`  :math:`y`
   ===============  ============================
   :math:`0,0`      :math:`0`
   :math:`0,1`      :math:`0`
   :math:`1,0`      :math:`0`
   :math:`1,1`      :math:`1`
   ===============  ============================

Binary Quadratic Models
=======================

D-Wave systems solve problems that can be mapped onto an Ising model or a quadratic
unconstrained binary optimization (QUBO) problem. These can be seen as subsets of a
binary quadratic model (BQM).

For example, the Boolean operations of logical gates represented as CSPs can also
be represented by a particular type of BQM called a penalty model: penalty functions
penalize invalid states; that is, invalid sets of input and output values representing gates
have higher penalty values than valid sets.

For example, the AND gate's constraint :math:`y=x_1x_2` can be represented as penalty function

.. math::

    x_1 x_2 - 2(x_1+x_2)y +3y,


which penalizes invalid configurations while no penalty is applied to valid configurations.

In Table `Boolean AND Operation as a Penalty`__\ , columns :math:`Out_{valid}` and :math:`Out_{invalid}`
represent, together with the :math:`in` column for each row, valid and invalid configurations
of an AND gate, with columns :math:`P_{valid}` and :math:`P_{invalid}` the respective penalty
values.

__ BooleanANDAsPenalty_

.. table:: Boolean AND Operation as a Penalty.
   :name: __BooleanANDAsPenalty

   ===========  ============================  ==============================  ===========================  ===
   **in**       :math:`\mathbf{out_{valid}}`  :math:`\mathbf{out_{invalid}}`   :math:`\mathbf{P_{valid}}`   :math:`\mathbf{P_{invalid}}`
   ===========  ============================  ==============================  ===========================  ===
   :math:`0,0`  :math:`0`                     :math:`1`                       :math:`0`                    :math:`3`
   :math:`0,1`  :math:`0`                     :math:`1`                       :math:`0`                    :math:`1`
   :math:`1,0`  :math:`0`                     :math:`1`                       :math:`0`                    :math:`1`
   :math:`1,1`  :math:`1`                     :math:`0`                       :math:`0`                    :math:`1`
   ===========  ============================  ==============================  ===========================  ===

For example, the state :math:`in=0,0; out_{valid}=0` of the first row is
represented by the penalty function with :math:`x_1=x_2=0` and
:math:`z = 0 = x_1 \wedge x_2`. For this valid configuration, the value of
:math:`P_{valid}` is

.. math::

    x_1 x_2 - 2(x_1+x_2)z +3z &= 0 \times 0 -2 \times (0+0) \times 0 + 3 \times 0

    &= 0,

not penalizing the valid configuration. In contrast, the state
:math:`in=0,0; out_{invalid}=1` of the same row is represented by the penalty
function with :math:`x_1=x_2=0` and :math:`z = 1 \ne x_1 \wedge x_2`. For this
invalid configuration, the value of :math:`P_{invalid}` is

.. math::

    x_1 x_2 - 2(x_1+x_2)z +3z &= 0 \times 0 -2 \times (0+0) \times 1 + 3 \times 1

    &= 3,

adding a penalty of :math:`3` to the incorrect configuration.

The samples representing low energy states returned from a sampler such as the D-Wave system
correspond to valid configurations, and therefore correctly represent the AND gate.

Example: Solving a Map-Coloring CSP
===================================

This example finds a solution to the map-coloring problem for a map of Canada
using four colors. Canada's 13 provinces are denoted by postal codes:

.. list-table:: Canadian Provinces' Postal Codes
   :widths: 10 20 10 20
   :header-rows: 1

   * - Code
     - Province
     - Code
     - Province
   * - AB
     - Alberta
     - BC
     - British Columbia
   * - MB
     - Manitoba
     - NB
     - New Brunswick
   * - NL
     - Newfoundland and Labrador
     - NS
     - Nova Scotia
   * - NT
     - Northwest Territories
     - NU
     - Nunavut
   * - ON
     - Ontario
     - PE
     - Prince Edward Island
   * - QC
     - Quebec
     - SK
     - Saskatchewan
   * - YT
     - Yukon
     -
     -

The workflow for solution is as follows:

#. Formulate the problem as a graph, with provinces represented as nodes and shared borders as edges,
   using 4 binary variables (one per color) for each province.
#. Create a binary constraint satisfaction problem and add all the needed constraints.
#. Convert to a binary quadratic model.
#. Sample.
#. Plot a valid solution, if such was found.

The following sample code creates a graph of the map with provinces as nodes and
shared borders between provinces as edges (e.g., "('AB', 'BC')" is an edge representing
the shared border between British Columbia and Alberta). It creates a binary constraint
satisfaction problem based on two types of constraints:

* :code:`csp.add_constraint(one_color_configurations, variables)` represents the constraint
  that each node (province) select a single color, as represented by valid configurations
  :code:`one_color_configurations = {(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)}`
* :code:`csp.add_constraint(not_both_1, variables)` represents the constraint that
  two nodes (provinces) with a shared edge (border) not both select the same color.


.. code-block:: python

    import dwavebinarycsp
    from dwave.system.samplers import DWaveSampler
    from dwave.system.composites import EmbeddingComposite
    import networkx as nx
    import matplotlib.pyplot as plt

    # Represent the map as the nodes and edges of a graph
    provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
    neighbors = [('AB', 'BC'), ('AB', 'NT'), ('AB', 'SK'), ('BC', 'NT'), ('BC', 'YT'), ('MB', 'NU'),
                 ('MB', 'ON'), ('MB', 'SK'), ('NB', 'NS'), ('NB', 'QC'), ('NL', 'QC'), ('NT', 'NU'),
                 ('NT', 'SK'), ('NT', 'YT'), ('ON', 'QC')]

    # Function for the constraint that two nodes with a shared edge not both select one color
    def not_both_1(v, u):
        return not (v and u)

    # Function that plots a returned sample
    def plot_map(sample):
        G = nx.Graph()
        G.add_nodes_from(provinces)
        G.add_edges_from(neighbors)
        # Translate from binary to integer color representation
        color_map = {}
        for province in provinces:
    	      for i in range(colors):
                if sample[province+str(i)]:
                    color_map[province] = i
        # Plot the sample with color-coded nodes
        node_colors = [color_map.get(node) for node in G.nodes()]
        nx.draw_circular(G, with_labels=True, node_color=node_colors, node_size=3000, cmap=plt.cm.rainbow)
        plt.show()

    # Valid configurations for the constraint that each node select a single color
    one_color_configurations = {(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)}
    colors = len(one_color_configurations)

    # Create a binary constraint satisfaction problem
    csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

    # Add constraint that each node (province) select a single color
    for province in provinces:
        variables = [province+str(i) for i in range(colors)]
        csp.add_constraint(one_color_configurations, variables)

    # Add constraint that each pair of nodes with a shared edge not both select one color
    for neighbor in neighbors:
        v, u = neighbor
	      for i in range(colors):
            variables = [v+str(i), u+str(i)]
		        csp.add_constraint(not_both_1, variables)

    # Convert the binary constraint satisfaction problem to a binary quadratic model
    bqm = dwavebinarycsp.stitch(csp)

    # Set up a solver using the local system’s default D-Wave Cloud Client configuration file
    # and sample 50 times
    sampler = EmbeddingComposite(DWaveSampler())         # doctest: +SKIP
    response = sampler.sample(bqm, num_reads=50)         # doctest: +SKIP

    # Plot the lowest-energy sample if it meets the constraints
    sample = next(response.samples())      # doctest: +SKIP
    if not csp.check(sample):              # doctest: +SKIP
        print("Failed to color map")
    else:
        plot_map(sample)


The plot shows a solution returned by the D-Wave solver. No provinces sharing a border
have the same color.

.. figure:: _images/map_coloring_CSP4colors.png
   :name: MapColoring_CSP4colors
   :alt: image
   :align: center
   :scale: 70 %

   Solution for a map of Canada with four colors. The graph comprises 13 nodes representing
   provinces connected by edges representing shared borders. No two nodes connected by
   an edge share a color.

Terminology
===========

.. glossary::

      model
          A collection of variables with associated linear and
          quadratic biases.

      sampler
          A process that samples from low energy states of a problem’s objective function.
          A binary quadratic model (BQM) sampler samples from low energy states in models such
          as those defined by an Ising equation or a Quadratic Unconstrained Binary Optimization
          (QUBO) problem and returns an iterable of samples, in order of increasing energy. A dimod
          sampler provides ‘sample_qubo’ and ‘sample_ising’ methods as well as the generic
          BQM sampler method.
