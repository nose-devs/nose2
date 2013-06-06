from nose2.tools.decorators import with_setup

setup_performed = False


def setup():
    global setup_performed
    setup_performed = True


@with_setup(setup)
def test_with_setup():
    assert setup_performed, 'Setup not performed.'
