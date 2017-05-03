import unittest
import pytest


# Tests
def test_foo(info):
    print("test_foo")
    assert True

def test_bar():
    print("test_bar")
    assert True

class Baz(unittest.TestCase):
    def test_baz(self):
        print("test_baz")
        assert True


# def get_baz():
#     class _Baz(unittest.TestCase):
#         def test_baz(self):
#             print("test_baz")
#             assert True
#
#     #test_case_class = type('Baz', (unittest.TestCase,), {})
#     return mark.usefixtures("info")(_Baz)
#
# SuperBaz = get_baz()


# Execute Tests
def main():


    class MyPlugin(object):
        def __init__(self, data):

            self.__name__ = "myplugin"
            self.data = data
            self.collected = set()

        def pytest_xdist_node_collection_finished(self, node, ids):
            self.collected.update(set(ids))

        def pytest_collection_modifyitems(self, items):
            for item in items:
                self.collected.update({item.nodeid})

        @pytest.fixture(autouse=True)
        def info(self, request):
            test = request.config.pluginmanager.get_plugin('myplugin')
            print("fixture: ", test.data)

    myplugin = MyPlugin('information')

    pytest.main(["test.py", "-s", '--collect-only'], plugins=[myplugin])
    pytest.main(["test.py", "-s"], plugins=[myplugin])

    print("Collected:", myplugin.collected)

if __name__ == "__main__":
    main()