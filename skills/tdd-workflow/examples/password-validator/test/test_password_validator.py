"""TDD 示例:红灯 → 绿灯 → 重构。

运行方式:
    python -m pytest test -q
"""

import pytest

from src.password_validator import validate_password


def test_valid_password_accepted():
    assert validate_password("abc12345") is True


def test_short_password_rejected():
    assert validate_password("abc12") is False


def test_no_digit_password_rejected():
    assert validate_password("abcdefgh") is False


def test_exact_min_length_accepted():
    assert validate_password("abcdefg1") is True


def test_empty_password_rejected():
    assert validate_password("") is False


def test_non_string_input_raises():
    with pytest.raises(TypeError):
        validate_password(None)
