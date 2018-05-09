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

install_requires = ['penaltymodel[all]>=0.14.0,<0.15.0',
                    'networkx>=2.0,<3.0',
                    'dimod>=0.6.7,<0.7.0'
                    'six>=1.11.0,<2.0.0']

packages = ['dwavebinarycsp',
            'dwavebinarycsp.compilers',
            'dwavebinarycsp.core',
            'dwavebinarycsp.factories',
            'dwavebinarycsp.factories.constraint',
            'dwavebinarycsp.factories.csp']

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
    install_requires=install_requires
)
