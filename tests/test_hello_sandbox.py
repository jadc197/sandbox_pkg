import sandbox_pkg


def test_resturns_str():
    assert isinstance(sandbox_pkg.hello_sandbox(), str)
