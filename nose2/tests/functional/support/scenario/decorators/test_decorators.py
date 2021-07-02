from nose2.tools.decorators import with_setup, with_teardown

setup_performed = False
teardown_performed = False


def setup():
    global setup_performed
    setup_performed = True


def teardown():
    global teardown_performed
    teardown_performed = True


@with_setup(setup)
def test_with_setup():
    assert setup_performed, "Setup not performed."


@with_teardown(teardown)
def test_with_teardown():
    pass


def test_teardown_ran():
    assert teardown_performed, "Teardown not performed."
