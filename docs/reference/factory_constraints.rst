.. _factory_constraints:

=========
Factories
=========

`dwavebinarycsp` currently provides factories for constraints representing
Boolean gates and satisfiability problems and CSPs for circuits and satisfiability
problems.

Constraints
===========

.. automodule:: dwavebinarycsp.factories.constraint

Gates
-----

.. autosummary::
   :toctree: generated/

   gates.and_gate
   gates.or_gate
   gates.xor_gate
   gates.halfadder_gate
   gates.fulladder_gate

Satisfiability Problems
-----------------------

.. autosummary::
   :toctree: generated/

   sat.sat2in4

CSPs
====

.. automodule:: dwavebinarycsp.factories.csp

.. autosummary::
   :toctree: generated/

   circuits.multiplication_circuit
   sat.random_2in4sat
   sat.random_xorsat
   
