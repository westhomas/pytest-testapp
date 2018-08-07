import unittest
import pytest


class MuhUnitTests(unittest.TestCase):

    def __init__(self):
        raise Exception("testing123")

    def test_passing(self):
        assert True


# Execute Tests
def main():
    pytest.main(['test_setup_exception.py', '-s'])


if __name__ == '__main__':
    main()
