.. _intro:

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

.. figure:: ../_static/Problem_MapColoring.png
   :name: Problem_MapColoring
   :alt: image
   :align: center
   :scale: 70 %

   Coloring a map of Canada with four colors.

The constraints for the map-coloring problem can be expressed as follows:

* Each region is assigned one color only, of :math:`C` possible colors.
* The color assigned to one region cannot be assigned to adjacent regions.

Solving this problem on a :term:`sampler` such as the D-Wave system necessitates that the
mathematical formulation use binary variables because the solution is implemented physically
with qubits, and so must translate to spins :math:`s_i\in\{-1,+1\}` or equivalent binary
values :math:`x_i\in \{0,1\}`. This means that in formulating the problem
by stating it mathematically, you might use unary encoding to represent the :math:`C` colors:
each region is represented by :math:`C` variables, one for each possible color, which
is set to value :math:`1` if selected, while the remaining :math:`C-1` variables are
:math:`0`.

Another example is logical circuits. Logic gates such as AND, OR, NOT, XOR etc
can be viewed as CSPs: the mathematically expressed relationships between inputs
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

The samples representing low energy states returned from a sampler such the D-Wave system
correspond to valid configurations, and therefore correctly represent the AND gate. 

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
