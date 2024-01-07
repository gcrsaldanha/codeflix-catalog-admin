from unittest.mock import MagicMock, create_autospec, patch

import pytest


class SumService:
    def sum(self, a, b):
        return a + b


class Calculator:
    def __init__(self, sum_service):
        self._sum_service = sum_service

    def make_sum(self, a, b):
        return self._sum_service.sum(a, b)


def test_calculator_without_mock():
    sum_service = SumService()
    calculator = Calculator(sum_service)

    assert calculator.make_sum(1, 2) == 3


def test_calculator_with_magic_mock():
    sum_service = MagicMock(SumService)  # Same as MagicMock(spec=SumService)
    sum_service.sum.return_value = 3

    # Calling a non-existent method fails
    with pytest.raises(AttributeError, match="Mock object has no attribute 'asdf'"):
        sum_service.asdf.return_value = 5

    # Does not fail despite method signature invalid, because has no autospec
    sum_service.sum(1, 2, 3, 4, 5)

    calculator = Calculator(sum_service)

    assert calculator.make_sum(1, 2) == 3


def test_with_create_autospec():
    sum_service = create_autospec(SumService)
    sum_service.sum.return_value = 3
    with pytest.raises(TypeError, match="too many positional arguments"):
        sum_service.sum(1, 2, 3, 4, 5)

    sum_service.sum.return_value = 3

    calculator = Calculator(sum_service)
    assert calculator.make_sum(1, 2) == 3


def test_with_mock_patch():
    # This creates a generic Mock
    with patch("example_mocking.SumService") as mock_sum_service:
        mock_sum_service.sum.return_value = 3

        calculator = Calculator(mock_sum_service)
        assert calculator.make_sum(1, 2) == 3

        # This method does not exist!
        mock_sum_service.multiply.return_value = 5
        assert mock_sum_service.multiply(1, 2) == 5  # This will pass


def test_with_mock_patch_and_spec():
    with patch("example_mocking.SumService", spec=SumService) as mock_sum_service:
        mock_sum_service.sum.return_value = 3

        calculator = Calculator(mock_sum_service)
        assert calculator.make_sum(1, 2) == 3

        # This method does not exist!
        with pytest.raises(AttributeError, match="Mock object has no attribute 'multiply'"):
            mock_sum_service.multiply.return_value = 5

        # But method signature is still not checked – non-recursive speccing
        mock_sum_service.sum(1, 2, 3, 4, 5)


def test_with_mock_patch_and_autospec():
    with patch("example_mocking.SumService", autospec=True) as mock_sum_service:
        mock_sum_service.sum.return_value = 3

        calculator = Calculator(mock_sum_service)
        assert calculator.make_sum(1, 2) == 3

        # This method does not exist!
        with pytest.raises(AttributeError, match="Mock object has no attribute 'multiply'"):
            mock_sum_service.multiply.return_value = 5

        # This signature is now checked!
        with pytest.raises(TypeError, match="too many positional arguments"):
            mock_sum_service.sum(1, 2, 3, 4, 5)


if __name__ == "__main__":
    test_calculator_without_mock()
    test_calculator_with_magic_mock()
    test_with_create_autospec()
    test_with_mock_patch()
    test_with_mock_patch_and_spec()
    test_with_mock_patch_and_autospec()
