
import getpass

from database.connection import DatabaseConnection
from modules.auth import verify_password
from modules.traveler import TravelerDashboard


def traveler_login():
    """Authenticate a registered traveler."""

    database = DatabaseConnection()
    connection = database.get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    try:
        print("\n--- TRAVELER LOGIN ---")

        email = input("Enter registered email: ").strip().lower()
        password = getpass.getpass("Enter password: ")

        cursor.execute(
            """
            SELECT traveler_id, full_name, email, phone, password_hash
            FROM travelers
            WHERE email = %s
            """,
            (email,)
        )

        traveler_data = cursor.fetchone()

        if traveler_data is None:
            print("Invalid email or password.")
            return

        traveler_id, name, traveler_email, phone, stored_hash = traveler_data

        if verify_password(password, stored_hash):
            print(f"\nWelcome, {name}!")
            print("Traveler login successful!")

            dashboard = TravelerDashboard(traveler_id, name)
            dashboard.display_menu()

        else:
            print("Invalid email or password.")

    except Exception as error:
        print(f"Login error: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    traveler_login()
