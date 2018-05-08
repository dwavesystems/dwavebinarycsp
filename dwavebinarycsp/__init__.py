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

from dwavebinarycsp.compilers import *
import dwavebinarycsp.compilers

from dwavebinarycsp.core import *
import dwavebinarycsp.core

from dwavebinarycsp.reduction import *
import dwavebinarycsp.reduction

import dwavebinarycsp.exceptions

import dwavebinarycsp.factories

from dwavebinarycsp.package_info import __version__, __author__, __authoremail__, __description__

import dwavebinarycsp.testing

# import dimod.Vartype, dimod.SPIN and dimod.BINARY into dwavebinarycsp namespace for convenience
from dimod import Vartype, SPIN, BINARY
