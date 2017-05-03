import pytest
from pytest import mark

#@pytest.mark.flaky(reruns=5)
def test_method4():
    import random
    assert random.choice([True, False, False, False])

# Execute Tests
def main():
    pytest.main(["test.py", "-s", '--reruns 5'])

if __name__ == "__main__":
    main()