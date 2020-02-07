.. _constraint_csp:

====================
Defining Constraints
====================

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
