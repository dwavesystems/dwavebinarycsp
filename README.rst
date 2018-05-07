.. image:: https://img.shields.io/pypi/v/dwavebinarycsp.svg
    :target: https://pypi.python.org/pypi/dwavebinarycsp

.. image:: https://coveralls.io/repos/github/dwavesystems/dwavebinarycsp/badge.svg?branch=master
    :target: https://coveralls.io/github/dwavesystems/dwavebinarycsp?branch=master

.. image:: https://readthedocs.org/projects/dwavebinarycsp/badge/?version=latest
    :target: http://dwavebinarycsp.readthedocs.io/en/latest/?badge=latest

.. image:: https://circleci.com/gh/dwavesystems/dwavebinarycsp.svg?style=svg
    :target: https://circleci.com/gh/dwavesystems/dwavebinarycsp

.. index-start-marker

dwavebinarycsp
========

todo

Example Usage
-------------

.. code-block:: python

    import dwavebinarycsp
    import dimod

    csp = dwavebinarycsp.factories.random_2in4sat(8, 4)  # 8 variables, 4 clauses

    bqm = dwavebinarycsp.stitch(csp)

    resp = dimod.ExactSolver().sample(bqm)

    for sample, energy in resp.data(['sample', 'energy']):
        print(sample, csp.check(sample), energy)

.. index-end-marker

Installation
------------

.. installation-start-marker

To install:

.. code-block:: bash

    pip install dwavebinarycsp

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
