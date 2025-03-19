.. _compilers_csp:

======================================
Converting to a Binary Quadratic Model
======================================

.. deprecated:: 0.3.1

    ``dwavebinarycsp`` is deprecated and will be removed in Ocean 10.
    For solving problems with constraints, we recommend using the hybrid
    solvers in the Leap service.
    You can find documentation for the hybrid solvers at :ref:`opt_index_hybrid`.

Constraint satisfaction problems can be converted to binary quadratic models to be solved
on samplers such as the D-Wave system.

.. currentmodule:: dwavebinarycsp

Compilers
=========

Compilers accept a constraint satisfaction problem and return a
:obj:`dimod.BinaryQuadraticModel`.

..
    DEV NOTE: in the future compilers should be organized by type. For instance stitch simply builds
    a bqm for each constraint and then adds them together. But other more sophisticated compilers
    might be 'structured' or 'embedding' or similar.

.. autosummary::
   :toctree: generated/

   stitch
