"""密码校验器。

规则:至少 8 位,且包含至少一个数字。
"""

MIN_LENGTH = 8


def validate_password(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    return len(password) >= MIN_LENGTH and any(c.isdigit() for c in password)




