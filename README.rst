:warning: *dwavebinarycsp* is deprecated. For solving problems with constraints,
    we recommend using the hybrid solvers in the Leap :tm: service. You can find
    documentation for the hybrid solvers at https://docs.ocean.dwavesys.com.

.. image:: https://img.shields.io/pypi/v/dwavebinarycsp.svg
    :target: https://pypi.org/project/dwavebinarycsp

.. image:: https://codecov.io/gh/dwavesystems/dwavebinarycsp/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dwavesystems/dwavebinarycsp

.. image:: https://circleci.com/gh/dwavesystems/dwavebinarycsp.svg?style=svg
    :target: https://circleci.com/gh/dwavesystems/dwavebinarycsp


==============
dwavebinarycsp
==============

.. start_binarycsp_about

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

.. end_binarycsp_about

Installation
============

To install:

.. code-block:: bash

    pip install dwavebinarycsp

To build from source:

.. code-block:: bash

    pip install -r requirements.txt
    python setup.py install

License
=======

Released under the Apache License 2.0. See LICENSE file.

Contributing
============

Ocean's `contributing guide <https://docs.dwavequantum.com/en/latest/ocean/contribute.html>`_
has guidelines for contributing to Ocean packages.