"""Minimal smoke tests — verify that the project modules load without errors."""


def test_import_solver():
    import solver  # noqa: F401
    assert True


def test_import_analysis():
    import analysis  # noqa: F401
    assert True


def test_import_verify():
    import verify  # noqa: F401
    assert True
