
from database.connection import DatabaseConnection
from modules.package_manager import PackageManager


def main():
    connection = DatabaseConnection().get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    manager = PackageManager(connection)

    try:
        print("\n--- PACKAGE TEST MENU ---")
        print("1. Add Package")
        print("2. View Packages")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Package name: ").strip()

            print("1. Single Destination")
            print("2. Multi Destination")

            package_choice = input("Choose package type: ").strip()

            if package_choice == "1":
                package_type = "Single Destination"
            elif package_choice == "2":
                package_type = "Multi Destination"
            else:
                print("Invalid package type.")
                return

            try:
                days = int(input("Duration in days: "))
                price = float(input("Base price in rupees: "))
            except ValueError:
                print("Enter valid numbers for days and price.")
                return

            description = input("Package description: ").strip()

            manager.add_package(
                name, package_type, days, price, description
            )

        elif choice == "2":
            manager.view_packages()

        elif choice == "0":
            print("Test completed.")

        else:
            print("Invalid choice.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
