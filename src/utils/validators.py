import re
from typing import Annotated

import phonenumbers
from pydantic import AfterValidator


def validate_phone(phone: str) -> str:
    try:
        parsed_number = phonenumbers.parse(phone, region="RU")
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number format")


PhoneStr = Annotated[str, AfterValidator(validate_phone)]


def validate_password(password: str) -> str:
    if not (6 <= len(password) <= 60):
        raise ValueError("Password length should be between 6 and 60 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("The password must contain at least one capital letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("The password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValueError("The password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("The password must contain at least one special character.")
    return password


PasswordStr = Annotated[str, AfterValidator(validate_password)]
