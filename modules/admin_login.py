
import getpass

from database.connection import DatabaseConnection
from modules.auth import verify_password
from modules.admin import Admin


def admin_login():
    """Authenticate the administrator."""

    database = DatabaseConnection()
    connection = database.get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    try:
        print("\n--- ADMIN LOGIN ---")

        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ")

        cursor.execute(
            """
            SELECT admin_id, username, password_hash
            FROM admins
            WHERE username = %s
            """,
            (username,)
        )

        admin_data = cursor.fetchone()

        if admin_data is None:
            print("Invalid username or password.")
            return

        admin_id, admin_username, stored_hash = admin_data

        if verify_password(password, stored_hash):
            print("\nAdmin login successful!")

            admin = Admin(admin_id, admin_username)
            admin.display_menu()

        else:
            print("Invalid username or password.")

    except Exception as error:
        print(f"Login error: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    admin_login()
