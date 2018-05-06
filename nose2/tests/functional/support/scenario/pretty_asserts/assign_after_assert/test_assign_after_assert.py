def test_demo():
    """
    Assign a value to `x` after an assert
    Testsuite will want to ensure that we print `x = 1`, which was the value at
    the time of the assert
    """
    x = 1
    assert x == 2
    x = 2
