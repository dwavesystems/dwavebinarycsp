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

_PY2 = sys.version_info.major == 2

# add __version__, __author__, __authoremail__, __description__ to this namespace
# equivalent to:
if _PY2:
    execfile("./dwavebinarycsp/package_info.py")
else:
    exec(open("./dwavebinarycsp/package_info.py").read())

# we prefer penaltymodel-mip over penaltymodel-maxgap, but mip cannot be used for python3.4 or for
# 32bit architectures
install_requires = ['penaltymodel>=0.15.0,<0.16.0',
                    'penaltymodel-cache>=0.3.0,<0.4.0',
                    'penaltymodel-maxgap>=0.4.0,<0.5.0; platform_machine == "x86" or python_version == "3.4"',
                    'penaltymodel-mip>=0.1.2,<0.2.0; platform_machine != "x86" and python_version != "3.4"',
                    'networkx>=2.0,<3.0',
                    'dimod>=0.6.7,<0.7.0'
                    'six>=1.11.0,<2.0.0']

packages = ['dwavebinarycsp',
            'dwavebinarycsp.compilers',
            'dwavebinarycsp.core',
            'dwavebinarycsp.factories',
            'dwavebinarycsp.factories.constraint',
            'dwavebinarycsp.factories.csp']

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
    install_requires=install_requires
)
