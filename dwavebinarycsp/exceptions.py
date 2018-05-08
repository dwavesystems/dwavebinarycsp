import penaltymodel as pm


class UnsatError(Exception):
    """Constraint or csp cannot be satisfied"""


class ImpossibleBQM(pm.ImpossiblePenaltyModel):
    """When a BQM cannot be built from a constraint/penaltymodel"""
