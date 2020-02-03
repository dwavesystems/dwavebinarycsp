.. image:: https://img.shields.io/pypi/v/dwavebinarycsp.svg
    :target: https://pypi.python.org/pypi/dwavebinarycsp

.. image:: https://ci.appveyor.com/api/projects/status/b99rhw0l6ljsgw5t?svg=true
    :target: https://ci.appveyor.com/project/dwave-adtt/dwavebinarycsp

.. image:: https://codecov.io/gh/dwavesystems/dwavebinarycsp/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dwavesystems/dwavebinarycsp

.. image:: https://readthedocs.com/projects/d-wave-systems-binarycsp/badge/?version=latest
    :target: https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/?badge=latest

.. image:: https://circleci.com/gh/dwavesystems/dwavebinarycsp.svg?style=svg
    :target: https://circleci.com/gh/dwavesystems/dwavebinarycsp

dwavebinarycsp
==============

.. index-start-marker

Library to construct a binary quadratic model from a constraint satisfaction problem with
small constraints over binary variables.

Below is an example usage:

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
