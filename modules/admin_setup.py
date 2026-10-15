
import getpass

from database.connection import DatabaseConnection
from modules.auth import hash_password


def create_admin():
    """Create the pre-configured admin account once."""

    database = DatabaseConnection()
    connection = database.get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT admin_id FROM admins LIMIT 1")

        if cursor.fetchone():
            print("Admin account already exists.")
            return

        print("\n--- CREATE ADMIN ACCOUNT ---")

        username = input("Enter admin username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        password = getpass.getpass("Enter admin password: ")
        confirm_password = getpass.getpass("Confirm admin password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO admins (username, password_hash)
            VALUES (%s, %s)
            """,
            (username, password_hash)
        )

        connection.commit()
        print("Admin account created successfully!")

    except Exception as error:
        connection.rollback()
        print(f"Admin setup error: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_admin()
