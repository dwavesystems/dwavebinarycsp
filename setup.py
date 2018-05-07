import sys
from setuptools import setup

_PY2 = sys.version_info.major == 2

# add __version__, __author__, __authoremail__, __description__ to this namespace
# equivalent to:
if _PY2:
    execfile("./dwavebinarycsp/package_info.py")
else:
    exec(open("./dwavebinarycsp/package_info.py").read())

install_requires = ['penaltymodel>=0.13.2,<0.14.0',
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
    url='https://github.com/dwavesystems/dwavebinarycsp',
    license='Apache 2.0',
    packages=packages,
    install_requires=install_requires
)
