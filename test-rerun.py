import unittest
import pytest
import random
from pytest import mark

#@pytest.mark.flaky(reruns=5)
# def test_method4():
#     assert random.choice([True, False, False, False])


def _build_test_case_class():
    test_case_class = type('Baz', (unittest.TestCase,), {})

    #@pytest.mark.flaky(reruns=5)
    def test_method(self):
        assert random.choice([True, False, False, False, False, False, False, False, False, False, False])

    test_method = mark.flaky(reruns=5)(test_method)

    setattr(test_case_class, "tester_testie", test_method)
    return test_case_class

TestCase = _build_test_case_class()


# Execute Tests
def main():
    pytest.main(["test-rerun.py", "-s", "--html=report.html", '--reruns', '5'])

if __name__ == "__main__":
    main()