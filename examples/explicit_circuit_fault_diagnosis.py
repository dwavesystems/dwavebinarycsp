import dwavebinarycsp

from dimod import ExactSolver


def xor_fault(a, b, out, fault):
    """Returns True if XOR(a, b) == out and fault == 0 or XOR(a, b) != out and fault == 1."""
    if (a != b) == out:
        return fault == 0
    else:
        return fault == 1


def and_fault(a, b, out, fault):
    """Returns True if AND(a, b) == out and fault == 0 or AND(a, b) != out and fault == 1."""
    if (a and b) == out:
        return fault == 0
    else:
        return fault == 1


def or_fault(a, b, out, fault):
    """Returns True if OR(a, b) == out and fault == 0 or OR(a, b) != out and fault == 1."""
    if (a or b) == out:
        return fault == 0
    else:
        return fault == 1


csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

# the first half adder
csp.add_constraint(xor_fault, ['A1', 'B1', 'S1/A2', 'xor_fault_1'])
csp.add_constraint(and_fault, ['A1', 'B1', 'C1', 'and_fault_1'])

# the second half adder
csp.add_constraint(xor_fault, ['S1/A2', 'B2', 'S2', 'xor_fault_2'])
csp.add_constraint(and_fault, ['S1/A2', 'B2', 'C2', 'and_fault_2'])

# finally the AND gate
csp.add_constraint(or_fault, ['C1', 'C2', 'ORout', 'or_fault'])


# now, say that the behaviour we witnessed was HA(0, 1, 0) -> 1, 1.
# The 'A' input to the circuit is 'A1'
csp.fix_variable('A1', 0)
# The 'B' input to the circuit is 'B1'
csp.fix_variable('B1', 1)
# the 'Cin' input to the circuit is 'B2'
csp.fix_variable('B2', 0)
# the sum output of the circuit is 'S2'
csp.fix_variable('S2', 1)
# the carry output of the circuit is 'ORout'
csp.fix_variable('ORout', 1)


# convert the csp to a bqm. We specify that the energy gap between the valid configurations and
# the invalid ones must be at least 2.0
bqm = dwavebinarycsp.stitch(csp, min_classical_gap=2.0)


# set up any dimod solver. In this case we use the ExactSolver but any unstructured solver would
# work.
sampler = ExactSolver()


# we can determine the minimum and maximum number of faults that will induce this behavior
response = sampler.sample(bqm)
min_energy = min(response.data_vectors['energy'])

fault_counts = []
for sample, energy in response.data(['sample', 'energy']):
    if csp.check(sample):
        n_faults = sum(sample[v] for v in sample if 'fault' in v)
        fault_counts.append(n_faults)
    else:
        # if the CSP is not satisfied, the energy should be above ground
        assert energy > min_energy

print('Minimum number of faults: ', min(fault_counts))
print('Maximum number of faults: ', max(fault_counts))

# If, instead of the ground states corresponding to all possible fault configurations, we
# instead only wanted to sample from minimum fault configurations, we need to bias against
# higher fault cardinalities. To do this, we add a small linear bias to the fault variables.
# We also make sure that the bias we add is less than 2.0, or else we would affect the energy
# levels.
bqm.add_variable('xor_fault_1', .5)  # if the variable is present, add_variable adds to the linear bias
bqm.add_variable('and_fault_1', .5)
bqm.add_variable('xor_fault_2', .5)
bqm.add_variable('and_fault_2', .5)
bqm.add_variable('or_fault', .5)

# now the samples that satisfy the csp and are minimum energy should be exactly the fault
# diagnosis with only a single fault
response = sampler.sample(bqm)
min_energy = min(response.data_vectors['energy'])

min_fault_diagnoses = []
for sample, energy in response.data(['sample', 'energy']):
    if csp.check(sample) and energy == min_energy:
        min_fault_diagnoses.append([v for v in sample if ('fault' in v and sample[v])])
    else:
        # if the CSP is not satisfied, the energy should be above ground
        assert energy > min_energy

print('min fault diagnoses: ', min_fault_diagnoses)
