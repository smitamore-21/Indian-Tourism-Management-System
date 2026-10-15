
def validate_name(name):
    return bool(name and name.strip())


def validate_email(email):
    if not email:
        return False

    return "@" in email and "." in email.rsplit("@", 1)[-1]


def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10


def validate_positive_number(value):
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False
