class Test:
    def __init__(self):
        raise RuntimeError(
            "Something bad happened but other tests should still be run!"
        )

    def test(self):
        raise RuntimeError(
            "Something bad happened but other tests should still be run! RUNNING"
        )
