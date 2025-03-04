.. _csp:

=========================================
Defining Constraint Satisfaction Problems
=========================================

.. deprecated:: 0.3.1

    ``dwavebinarycsp`` is deprecated and will be removed in Ocean 10.
    For solving problems with constraints, we recommand using the hybrid
    solvers in the Leap service.
    You can find documentation for the hybrid solvers at :ref:`opt_index_hybrid`.

.. automodule:: dwavebinarycsp.core.csp

Class
=====

.. currentmodule:: dwavebinarycsp
.. autoclass:: ConstraintSatisfactionProblem


Methods
=======

Adding variables and constraints
--------------------------------

.. autosummary::
   :toctree: generated/

   ConstraintSatisfactionProblem.add_constraint
   ConstraintSatisfactionProblem.add_variable


Satisfiability
--------------

.. autosummary::
   :toctree: generated/

   ConstraintSatisfactionProblem.check


Transformations
---------------

.. autosummary::
   :toctree: generated/

   ConstraintSatisfactionProblem.fix_variable
