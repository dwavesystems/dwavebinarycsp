from __future__ import absolute_import

from dimod.template_sampler import TemplateSampler

from dwave_constraint_compilers.compilers import stitch
from dwave_constraint_compilers.constraint_specification_languages.internal import validate
from dwave_constraint_compilers.utils import constraint_vartype, sample_vartype, convert_sample

__all__ = ['satisfy']


def satisfy(constraints, sampler, compilation_method=stitch, validate_constraints=True, **sampler_args):

    assert isinstance(sampler, TemplateSampler), "Expected sampler to be a subclass of 'TemplateSampler"
    if validate_constraints:
        validate(constraints)

    # Figure out the Vartype now, in case the compilation method changes it. We'll need this to determine
    # what Vartype to return. For simplicity, let's assume the Vartype of the first constraint dictates
    # the Vartype for all of them.
    original_vartype = constraint_vartype(constraints[0])

    bqm = compilation_method(constraints)

    response = sampler.sample_ising(bqm.linear, bqm.quadratic, **sampler_args)

    # dimod samplers return dimod responses, which keep their samples sorted by increasing energy.
    # get the sample with lowest energy.
    sample = next(iter(response))

    if original_vartype != sample_vartype(sample):
        sample = convert_sample(sample, vartype=original_vartype)

    return sample
