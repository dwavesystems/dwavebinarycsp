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
from setuptools.command.install import install

_PY2 = sys.version_info.major == 2

# add __version__, __author__, __authoremail__, __description__ to this namespace
# equivalent to:
if _PY2:
    execfile("./dwavebinarycsp/package_info.py")
else:
    exec(open("./dwavebinarycsp/package_info.py").read())


class PenaltyModelCheck(install):
    """Check that at least one of penaltymodel-{mip,maxgap} is installed."""

    def run(self):
        install.run(self)

        # For `dwavebinarycsp` to be functional, at least one penalty model
        # factory has to be installed. Decision on which is up to the user
        # (see the note above `extras_require`).

        try:
            from penaltymodel.core import iter_factories

            factories = iter_factories()

            # penaltymodel-cache is one
            next(factories)

            # but we require also mip or maxgap
            next(factories)

        except StopIteration:
            raise RuntimeError(
                "At least one penaltymodel factory must be specified. Try "
                "'pip install dwavebinarycsp[mip]' or 'pip install dwavebinarycsp[maxgap]'.")


install_requires = [
    'penaltymodel>=0.15.0,<0.16.0',
    'penaltymodel-cache>=0.3.0,<0.4.0',
    'networkx>=2.0,<3.0',
    'dimod>=0.6.7,<0.8.0',
    'six>=1.11.0,<2.0.0',
]

# We prefer penaltymodel-mip over penaltymodel-maxgap, but mip cannot be used
# for python3.4 or for 32bit pythons (running on either 32- or 64-bit architectures).
#
# Since it's currently impossible to test for "bitness" of the interpreter via
# PEP-508 environment markers (note: it is possible to run 32-bit python on
# 64-bit platform; and that's the case we can't catch), we delegate the selection
# of penaltymodel factory to the user (or the caller; e.g. `dwave-ocean-sdk` installer).
extras_require = {
    'mip': [
        'penaltymodel-mip>=0.1.2,<0.2.0'
    ],
    'maxgap': [
        'penaltymodel-maxgap>=0.4.0,<0.5.0'
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
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

python_requires = '>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*'

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
    cmdclass={'install': PenaltyModelCheck},
    zipsafe=False,
)
