from nose2.tools.params import params

# fmt: off


# multiline function definition
def test_demo(
):
    x = 1
    y = 2
    assert x > y, "oh noez, x <= y"


@params(('foo',),
        ('bar',))
def test_multiline_deco(value):
    assert not value
# fmt: on
