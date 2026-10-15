
import getpass

from database.connection import DatabaseConnection
from modules.auth import hash_password
from utils.validators import (
    validate_name,
    validate_email,
    validate_phone
)


def register_traveler():
    """Register a new traveler."""

    database = DatabaseConnection()
    connection = database.get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    try:
        print("\n--- TRAVELER REGISTRATION ---")

        name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip().lower()
        phone = input("Enter 10-digit phone number: ").strip()

        if not validate_name(name):
            print("Name cannot be empty.")
            return

        if not validate_email(email):
            print("Enter a valid email address.")
            return

        if not validate_phone(phone):
            print("Phone number must contain exactly 10 digits.")
            return

        password = getpass.getpass("Create password: ")
        confirm_password = getpass.getpass("Confirm password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO travelers
            (full_name, email, phone, password_hash)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, phone, password_hash)
        )

        connection.commit()
        print("Traveler registered successfully!")

    except Exception as error:
        connection.rollback()
        print(f"Registration error: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    register_traveler()
