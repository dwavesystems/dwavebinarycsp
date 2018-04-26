.. _compilers:

======================================
Converting to a Binary Quadratic Model
======================================

Constraint satisfaction problems can be converted to binary quadratic models to be solved.

.. currentmodule:: dwavecsp

Compilers
=========

Each compiler accepts a constraint satisfaction problem and returns a
:obj:`dimod.BinaryQuadraticModel`.

..
    DEV NOTE: in the future compilers should be organized by type. For instance stitch simply builds
    a bqm for each constraint and then adds them together. But other more sophisticated compilers
    might be 'structured' or 'embedding' or similar.

.. autosummary::
   :toctree: generated/

   stitch
