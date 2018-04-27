.. image:: https://circleci.com/gh/arcondello/dwavecsp.svg?style=svg
    :target: https://circleci.com/gh/arcondello/dwavecsp
    :alt: circle-ci Status

.. image:: https://coveralls.io/repos/github/dwavesystems/dwave_constraint_compilers/badge.svg?branch=master
    :target: https://coveralls.io/github/dwavesystems/dwave_constraint_compilers?branch=master
    :alt: Coverage Report

.. image:: https://readthedocs.org/projects/dwave_constraint_compilers/badge/?version=latest
    :target: http://dwave_constraint_compilers.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. index-start-marker

dwavecsp
========

todo

Example Usage
-------------

.. code-block:: python

    import dwavecsp
    import dimod

    csp = dwavecsp.factories.random_2in4sat(8, 4)  # 8 variables, 4 clauses

    bqm = dwavecsp.stitch(csp)

    resp = dimod.ExactSolver().sample(bqm)

    for sample, energy in resp.data(['sample', 'energy']):
        print(sample, csp.check(sample), energy)

.. index-end-marker

Installation
------------

.. installation-start-marker

To install:

.. code-block:: bash

    pip install dwavecsp

To build from source:

.. code-block:: bash
    
    pip install -r requirements.txt
    python setup.py install

.. installation-end-marker

License
-------

Released under the Apache License 2.0. See LICENSE file.

Contribution
------------

See CONTRIBUTING.rst file.
