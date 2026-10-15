
from database.setup_database import DatabaseSetup
from database.connection import DatabaseConnection
from utils.helpers import display_title


def test_database_connection():
    """Check whether the database connection works."""
    database = DatabaseConnection()
    connection = database.get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    print("Database connection successful!")
    connection.close()


def main():
    """Start the Indian Tourism Management System."""

    while True:
        display_title("INDIAN TOURISM MANAGEMENT SYSTEM")

        print("\n1. Setup Database")
        print("2. Test Database Connection")
        print("3. Admin Login")
        print("4. Traveler Registration")
        print("5. Traveler Login")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            setup = DatabaseSetup()
            setup.create_database()

        elif choice == "2":
            test_database_connection()

        elif choice == "3":
            from modules.admin_login import admin_login
            admin_login()

        elif choice == "4":
            from modules.traveler_registration import register_traveler
            register_traveler()

        elif choice == "5":
            from modules.traveler_login import traveler_login
            traveler_login()

        elif choice == "0":
            print("Thank you for using our system!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
