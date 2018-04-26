.. _csp:

=========================================
Defining Constraint Satisfaction Problems
=========================================


Overview
========
.. automodule:: dwavecsp.core.csp

.. currentmodule:: dwavecsp
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
