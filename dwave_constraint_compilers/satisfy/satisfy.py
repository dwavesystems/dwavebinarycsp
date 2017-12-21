from __future__ import absolute_import

from dwave_constraint_compilers.compilers import stitch
from dwave_constraint_compilers.constraint_specification_languages.internal import validate
from dwave_constraint_compilers.utils import constraint_vartype, sample_vartype, convert_sample, iteritems

__all__ = ['satisfy', 'is_satisfied', 'iter_unsatisfied_constraints']


def satisfy(constraints, sampler, compilation_method=stitch, validate_constraints=True, **sampler_args):
    """todo"""

    # check the the sampler is a dimod-compliant sampler
    # Author note: we want to handle samplers that have the same API as a dimod sampler but are not
    # themselves a subclass of the dimod TemplateSampler.
    if not hasattr(sampler, "sample_qubo") or not callable(sampler.sample_qubo):
        raise TypeError("expected sampler to have a 'sample_qubo' method")
    if not hasattr(sampler, "sample_ising") or not callable(sampler.sample_ising):
        raise TypeError("expected sampler to have a 'sample_ising' method")

    if validate_constraints:
        validate(constraints)

    # Figure out the Vartype now, in case the compilation method changes it. We'll need this to determine
    # what Vartype to return. For simplicity, let's assume the Vartype of the first constraint dictates
    # the Vartype for all of them.
    original_vartype = constraint_vartype(next(iter(constraints.values())))

    bqm = compilation_method(constraints)

    response = sampler.sample_ising(bqm.linear, bqm.quadratic, **sampler_args)

    # dimod samplers return dimod responses, which keep their samples sorted by increasing energy.
    # get the sample with lowest energy.
    sample = next(iter(response))

    if original_vartype != sample_vartype(sample):
        sample = convert_sample(sample, vartype=original_vartype)

    return sample


def is_satisfied(constraints, sample):
    """todo"""
    return not any(iter_unsatisfied_constraints(constraints, sample))


def iter_unsatisfied_constraints(constraints, sample):
    for label, constraint in iteritems(constraints):
        config = tuple(sample[v] for v in constraint['variables'])
        if config not in constraint['feasible_configurations']:
            yield label
