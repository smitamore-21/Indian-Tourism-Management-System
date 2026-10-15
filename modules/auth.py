
import hashlib
import hmac
import os


def hash_password(password):
    """Create a salted PBKDF2 password hash."""
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex() + "$" + password_hash.hex()


def verify_password(password, stored_hash):
    """Verify a password against its stored hash."""
    try:
        salt_hex, hash_hex = stored_hash.split("$", 1)
        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        )

        return hmac.compare_digest(
            password_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False
