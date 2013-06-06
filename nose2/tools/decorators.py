def with_setup(setup):
    def decorator(testcase):
        testcase.setup = setup

        return testcase

    return decorator
