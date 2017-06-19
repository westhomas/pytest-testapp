import pytest
from _pytest.config import get_plugin_manager


# Tests

def test_foo():
    assert True

def test_bar():
    assert True


# Plugins

def pytest_configure(config):
    config.pluginmanager.register(MyPlugin())

class MyPlugin(object):
    def __init__(self):
        self.__name__ = "myplugin"
        self.collected = set()

    def pytest_runtest_call(self, item):
        print('pytest_runtest_call')
        print('item: %s' % item)

    def pytest_xdist_node_collection_finished(self, node, ids):
        self.collected.update(set(ids))
        print('pytest_xdist_node_collection_finished')

    def pytest_collection_modifyitems(self, items):
        print('pytest_collection_modifyitems')
        for item in items:
            self.collected.update({item.nodeid})
            

# Execute Tests
def main():

    # This run causes `pytest_runtest_call` to fire
    args = ["test-plugin.py", "-s",]
    pytest.main(args)

    # This run will not fire `pytest_runtest_call`
    args += "-d --tx 4*popen//python=python3".split(' ')
    pytest.main(args)


    # Gather data about execution
    mgr = get_plugin_manager()
    myplugin = mgr.getplugin("myplugin")
    print("Collected:", myplugin.collected)

if __name__ == "__main__":
    main()