.. _constraint_csp:

====================
Defining Constraints
====================

.. deprecated:: 0.3.1

    ``dwavebinarycsp`` is deprecated and will be removed in Ocean 10.
    For solving problems with constraints, we recommand using the hybrid
    solvers in the Leap service.
    You can find documentation for the hybrid solvers at :ref:`using_hybrid`.

.. automodule:: dwavebinarycsp.core.constraint

Class
=====

.. currentmodule:: dwavebinarycsp
.. autoclass:: Constraint


Methods
=======

Construction
------------

.. autosummary::
   :toctree: generated/

   Constraint.from_configurations
   Constraint.from_func

Satisfiability
--------------

.. autosummary::
   :toctree: generated/

   Constraint.check

Transformations
---------------

.. autosummary::
   :toctree: generated/

   Constraint.fix_variable
   Constraint.flip_variable

Copies and projections
----------------------

.. autosummary::
   :toctree: generated/

   Constraint.copy
   Constraint.projection
