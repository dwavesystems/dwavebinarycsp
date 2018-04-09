import sys
from setuptools import setup

_PY2 = sys.version_info.major == 2

# add __version__, __author__, __authoremail__, __description__ to this namespace
# equivalent to:
# from dwave_constraint_compilers.packaing_info import *
if _PY2:
    execfile("./dwave_constraint_compilers/package_info.py")
else:
    exec(open("./dwave_constraint_compilers/package_info.py").read())

install_requires = ['penaltymodel>=0.13.2,<0.14.0',
                    'networkx>=2.0,<3.0',
                    'jsonschema>=2.6.0,<3.0.0',
                    'dimod>=0.6.7,<0.7.0'
                    'six>=1.11.0,<2.0.0']

packages = ['dwave_constraint_compilers',
            'dwave_constraint_compilers.compilers',
            'dwave_constraint_compilers.satisfy',
            'dwave_constraint_compilers.constraint_specification_languages']

setup(
    name='dwave_constraint_compilers',
    version=__version__,
    author=__author__,
    author_email=__authoremail__,
    description=__description__,
    url='https://github.com/dwavesystems/dwave_constraint_compilers',
    license='Apache 2.0',
    packages=packages,
    install_requires=install_requires,
    include_package_data=True
)
