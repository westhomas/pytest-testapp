import io
import logging
import subprocess
from contextlib import redirect_stderr, redirect_stdout

import pytest

from utils import quiet

logger = logging.getLogger(__name__)


# TODO: Add this to your conftest.py
# pytest_plugins = ["test_xdist_exception",]

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    raise Exception('this exception is hidden by xdist in parallel mode')

# Tests
def test_foo():
    assert True


def test_foo2():
    assert True


# Doesn't work
@quiet
def main():

    msg = ""

    with io.StringIO() as error_buff, \
            io.StringIO() as out_buff, \
            redirect_stderr(error_buff), \
            redirect_stdout(out_buff):

        returncode = pytest.main(['test_xdist_exception.py', '--html={}'.format('testing.html'), '-d', '--tx', '{}*popen//python=python3'.format(2), ])

        if returncode > 1 and returncode != 5:
            msg = "CRITICAL FAILURE RUNNING PYTEST: return code: {}\n".format(returncode)

        error = error_buff.getvalue()
        log_standard = out_buff.getvalue()

    print("CAPTURED ERROR")
    print("===============================")
    print(error)
    print("CAPTURED LOGS")
    print("===============================")
    print(log_standard)
    print(msg)


# Works - but there's no stderr
@quiet
def main2():
    msg = ""

    with io.StringIO() as error_buff, \
            io.StringIO() as out_buff, \
            redirect_stderr(error_buff), \
            redirect_stdout(out_buff):

        returncode = pytest.main(['test_xdist_exception.py', '--html={}'.format('testing.html'), ])

        if returncode > 1 and returncode != 5:
            msg = "CRITICAL FAILURE RUNNING PYTEST: return code: {}\n".format(returncode)

        error = error_buff.getvalue()
        log_standard = out_buff.getvalue()

    print("CAPTURED ERROR")
    print("===============================")
    print(error)
    print("CAPTURED LOGS")
    print("===============================")
    print(log_standard)
    print(msg)


# Works
@quiet
def main3():

    p = subprocess.run(['py.test', 'test_xdist_exception.py', '--html={}'.format('testing.html'), '-d', '--tx', '{}*popen//python=python3'.format(2), ],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    out = p.stdout.decode()
    err = p.stderr.decode()

    print("CAPTURED ERROR")
    print("===============================")
    print(err)
    print("CAPTURED LOGS")
    print("===============================")
    print(out)


# Testing redirecting stdour/err
# Works
@quiet
def main4():

    with io.StringIO() as error_buff, \
            io.StringIO() as out_buff, \
            redirect_stderr(error_buff), \
            redirect_stdout(out_buff):

        import sys

        sys.stdout.write('Hello World\n')
        sys.stdout.flush()
        sys.stderr.write('Im an error\n')
        sys.stderr.flush()

        log_standard = out_buff.getvalue()
        error = error_buff.getvalue()

    print("CAPTURED ERROR")
    print("===============================")
    print(error)
    print("CAPTURED LOGS")
    print("===============================")
    print(log_standard)
    print("DONE")





if __name__ == '__main__':
    main()
