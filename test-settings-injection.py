import pytest

from settings import base as settings_base


# Tests
def test_foo():
    assert settings_base.settings.IMPORTANT_SETTING == 'parallel value'


def test_foo2():
    assert settings_base.settings.IMPORTANT_SETTING == 'parallel value'


@pytest.mark.serial
def test_bar():
    assert settings_base.settings.IMPORTANT_SETTING == 'serial value'


# Execute Tests
def main():
    class MyPlugin(object):
        def __init__(self):
            self.__name__ = 'myplugin'
            self.collected = set()

        def pytest_xdist_node_collection_finished(self, node, ids):
            self.collected.update(set(ids))

        def pytest_collection_modifyitems(self, items):
            for item in items:
                self.collected.update({item.nodeid})

        def pytest_configure(self, config):
            # mutate setting value
            from settings import base as settings_base
            settings_base.settings.IMPORTANT_SETTING = 'serial value'

        def pytest_testnodeready(self, node):
            # mutate setting value
            from settings import base as settings_base
            settings_base.settings.IMPORTANT_SETTING = 'parallel value'

    # this works
    myplugin = MyPlugin()
    pytest.main(['test-settings-injection.py', '-s', '-m', 'serial'], plugins=[myplugin])
    print('Serial Collected:', myplugin.collected)

    # this doesn't work
    myplugin = MyPlugin()
    pytest.main(['test-settings-injection.py', '-s', '-m', 'not serial', '-d', '--tx', '{}*popen//python=python3'.format(2), ], plugins=[myplugin])
    print('Parallel (threads) Collected:', myplugin.collected)

    # this doesn't work
    myplugin = MyPlugin()
    pytest.main(['test-settings-injection.py', '-s', '-m', 'not serial', '-n2', ], plugins=[myplugin])
    print('Parallel (CPUs) Collected:', myplugin.collected)


if __name__ == '__main__':
    main()
