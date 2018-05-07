import itertools

from dimod import Vartype

from dwavebinarycsp.core import Constraint


def assert_consistent_constraint(const):
    assert isinstance(const, Constraint)

    assert hasattr(const, 'configurations')
    assert isinstance(const.configurations, frozenset)

    assert hasattr(const, 'func')
    assert callable(const.func)

    assert hasattr(const, 'variables')
    assert isinstance(const.variables, tuple)

    assert len(const) == len(const.variables)

    assert hasattr(const, 'vartype')
    assert isinstance(const.vartype, Vartype)

    for config in const.configurations:
        assert isinstance(config, tuple)
        assert len(config) == len(const.variables)

        msg = "config {} does not match constraint vartype '{}'".format(config, const.vartype)
        assert set(config).issubset(const.vartype.value), msg

        assert const.func(*config), 'Constraint.func does not evaluate True for {}'.format(config)
        assert const.check(dict(zip(const.variables, config)))

    for config in itertools.product(const.vartype.value, repeat=len(const)):
        if config in const.configurations:
            assert const.func(*config)
            assert const.check(dict(zip(const.variables, config)))
        else:
            assert not const.func(*config)
            assert not const.check(dict(zip(const.variables, config)))
