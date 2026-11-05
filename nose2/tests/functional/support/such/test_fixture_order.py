from nose2.tools import such


def add_fixtures(name):
    @it.has_test_setup
    def setup_first():
        print(f"{name} setup 1")

    @it.has_test_setup
    def setup_second(case):
        print(f"{name} setup 2")

    @it.has_test_teardown
    def teardown_first():
        print(f"{name} teardown 1")

    @it.has_test_teardown
    def teardown_second(case):
        print(f"{name} teardown 2")


with such.A("parent") as it:
    add_fixtures("parent")

    @it.should("run parent fixtures")
    def parent_test():
        print("parent test")

    with it.having("child"):
        add_fixtures("child")

        @it.should("run child fixtures")
        def child_test():
            print("child test")

        with it.having("grandchild"):
            add_fixtures("grandchild")

            @it.should("run grandchild fixtures")
            def grandchild_test():
                print("grandchild test")

            @it.should("clean up after a failure")
            def failing_test():
                print("failing test")
                raise AssertionError("intentional failure")

    with it.having("no fixtures of its own"):

        @it.should("inherit parent fixtures")
        def inherited_test():
            print("inherited test")


it.createTests(globals())
