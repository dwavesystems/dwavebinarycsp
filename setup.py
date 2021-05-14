# Copyright 2018 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# ================================================================================================

import sys
from setuptools import setup

# add __version__, __author__, __authoremail__, __description__ to this namespace
# equivalent to:
exec(open("./dwavebinarycsp/package_info.py").read())


install_requires = [
    'penaltymodel>=0.16.0,<0.17.0',
    'penaltymodel-cache>=0.4.0,<0.5.0',
    'penaltymodel-lp>=0.1.0,<0.2.0',
    'networkx>=2.0,<3.0',
    'dimod>=0.6.7,<0.10.0',
    'six>=1.11.0,<2.0.0',
]

# For `dwavebinarycsp` to be functional, at least one penalty model factory has
# to be installed. Decision on which is up to the user.
#
# We prefer penaltymodel-mip over penaltymodel-maxgap, but mip cannot be used
# for python3.4 or for 32bit pythons (running on either 32- or 64-bit architectures).
#
# Since it's currently impossible to test for "bitness" of the interpreter via
# PEP-508 environment markers (note: it is possible to run 32-bit python on
# 64-bit platform; and that's the case we can't catch), we delegate the selection
# of penaltymodel factory to the user (or the caller; e.g. `dwave-ocean-sdk` installer).
extras_require = {
    'mip': [
        'penaltymodel-mip>=0.2.0,<0.3.0'
    ],
    'maxgap': [
        'penaltymodel-maxgap>=0.5.0,<0.6.0'
    ]
}

packages = [
    'dwavebinarycsp',
    'dwavebinarycsp.compilers',
    'dwavebinarycsp.core',
    'dwavebinarycsp.factories',
    'dwavebinarycsp.factories.constraint',
    'dwavebinarycsp.factories.csp',
    'dwavebinarycsp.io',
]

classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
]

python_requires = '>=3.6'

setup(
    name='dwavebinarycsp',
    version=__version__,
    author=__author__,
    author_email=__authoremail__,
    description=__description__,
    long_description=open('README.rst').read(),
    url='https://github.com/dwavesystems/dwavebinarycsp',
    license='Apache 2.0',
    packages=packages,
    classifiers=classifiers,
    python_requires=python_requires,
    install_requires=install_requires,
    extras_require=extras_require,
)
