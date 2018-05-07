.. _compilers:

======================================
Converting to a Binary Quadratic Model
======================================

Constraint satisfaction problems can be converted to binary quadratic models to be solved
on samplers such as the D-Wave system.

.. currentmodule:: dwavecsp

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
