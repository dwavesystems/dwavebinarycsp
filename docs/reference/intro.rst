.. _intro:

============
Introduction
============

`dwavebinarycsp` is a library to construct a binary quadratic :term:`model` from a constraint
satisfaction problem (CSP) with small constraints over binary variables (represented
as either binary values {0, 1} or spint values {-1, 1}).

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

The constraints for the map-coloring problem can be expressed as

* Each region is assigned one color only, of :math:`C` possible colors.
* The color assigned to one region cannot be assigned to adjacent regions.

Solving such a problem on a :term:`sampler` such as the D-Wave system necessitates that the
mathematical formulation use binary variables because the solution is implemented physically
with qubits, and so must translate to spins :math:`s_i\in\{-1,+1\}` or equivalent binary
values :math:`x_i\in \{0,1\}`. This means that in formulating the problem
by stating it mathematically---for example, representing the possible set of colors
with variables---you might, instead of the more intuitive numerical scheme of natural numbers
for values, use unary encoding to represent the :math:`C` possible colors:
each region is represented by :math:`C` variables, one for each possible color, which
is set to value :math:`1` if selected, while the remaining :math:`C-1` variables are
:math:`0`.

Another example is logical circuits. Logic gates such as AND, OR, NOT, XOR etc
can be viewed as CSPs: the mathematically expressed relationships between inputs
and outputs must meet certain validity conditions. For inputs :math:`x_1,x_2` and
output :math:`y` of an AND gate, the constraint that must be satisfied, :math:`y=x_1x_2`,
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
