import subprocess

import pytest

from utils import quiet
from settings import base as settings_base


# TODO: Add this to your conftest.py
# pytest_plugins = ["test_settings_injection",]


def pytest_sessionstart(session):
    from settings import base as settings_base
    if hasattr(session.config, 'workerinput'):
        settings_base.settings.IMPORTANT_SETTING = 'parallel value'
    else:
        settings_base.settings.IMPORTANT_SETTING = 'serial value'


# Tests
def test_foo():
    assert settings_base.settings.IMPORTANT_SETTING == 'parallel value'


def test_foo2():
    assert settings_base.settings.IMPORTANT_SETTING == 'parallel value'


@pytest.mark.serial
def test_bar():
    assert settings_base.settings.IMPORTANT_SETTING == 'serial value'


# Execute Tests
@quiet
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

    # Run pytest inline with serial tests
    myplugin = MyPlugin()
    pytest.main(['test_settings_injection.py', '-s', '-m', 'serial'], plugins=[myplugin])
    print('Serial Collected:', myplugin.collected)

    # Run pytest inline with parallel tests
    myplugin = MyPlugin()
    pytest.main(['test_settings_injection.py', '-s', '-m', 'not serial', '-d', '--tx', '{}*popen//python=python3'.format(2), ], plugins=[myplugin])
    print('Parallel Collected:', myplugin.collected)

    # Run pytest subprocess with serial tests
    subprocess.check_call(['py.test', 'test_settings_injection.py', '-m', 'serial', ])

    # Run pytest subprocess with parallel tests
    subprocess.check_call(['py.test', 'test_settings_injection.py', '-m', 'not serial', '-d', '--tx', '{}*popen//python=python3'.format(2), ])


if __name__ == '__main__':
    main()
