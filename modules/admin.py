
"""
Admin Module
Handles administrator operations for destinations and packages.
"""

from database.connection import DatabaseConnection
from modules.destination_manager import DestinationManager
from modules.package_manager import PackageManager
from modules.reports import Reports


class Admin:
    """Represent an administrator."""

    def __init__(self, admin_id, username):
        self.admin_id = admin_id
        self.username = username

    def display_menu(self):
        """Display and handle the admin menu."""

        while True:
            print("\n--- ADMIN MENU ---")
            print("1. Manage Destinations")
            print("2. Manage Packages")
            print("3. View Bookings")
            print("4. View Reports")
            print("0. Logout")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.manage_destinations()

            elif choice == "2":
                self.manage_packages()

            elif choice == "3":
                print("Booking management will be connected next.")

            elif choice == "4":
                self.view_reports()

            elif choice == "0":
                print("Admin logged out successfully.")
                break

            else:
                print("Invalid choice. Please try again.")

    def view_reports(self):
        """Display available booking reports."""

        connection = DatabaseConnection().get_connection()

        if connection is None:
            print("Database connection failed.")
            return

        try:
            reports = Reports(connection)

            while True:
                print("\n--- VIEW REPORTS ---")
                print("1. Confirmed Booking Revenue")
                print("2. Package Booking Count")
                print("0. Back to Admin Menu")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    reports.total_booking_revenue()

                elif choice == "2":
                    reports.package_booking_count()

                elif choice == "0":
                    break

                else:
                    print("Invalid choice. Please try again.")

        finally:
            connection.close()

    def manage_destinations(self):
        """Add, view, update and delete destinations."""

        connection = DatabaseConnection().get_connection()

        if connection is None:
            print("Database connection failed.")
            return

        manager = DestinationManager(connection)

        try:
            while True:
                print("\n--- MANAGE DESTINATIONS ---")
                print("1. Add Destination")
                print("2. View Destinations")
                print("3. Update Destination")
                print("4. Delete Destination")
                print("0. Back to Admin Menu")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    name = input("Destination name: ").strip()
                    state = input("State: ").strip()
                    description = input("Description: ").strip()

                    if not name or not state or not description:
                        print("All fields are required.")
                        continue

                    try:
                        distance = float(input("Distance in km: "))

                        if distance < 0:
                            print("Distance cannot be negative.")
                            continue

                    except ValueError:
                        print("Enter a valid distance.")
                        continue

                    manager.add_destination(
                        name, state, description, distance
                    )

                elif choice == "2":
                    manager.view_destinations()

                elif choice == "3":
                    try:
                        destination_id = int(
                            input("Destination ID to update: ")
                        )
                        distance = float(
                            input("Updated distance in km: ")
                        )

                        if destination_id <= 0 or distance < 0:
                            print("Enter a valid ID and distance.")
                            continue

                    except ValueError:
                        print("Enter valid numeric values.")
                        continue

                    name = input("Updated name: ").strip()
                    state = input("Updated state: ").strip()
                    description = input("Updated description: ").strip()

                    if not name or not state or not description:
                        print("All fields are required.")
                        continue

                    manager.update_destination(
                        destination_id,
                        name,
                        state,
                        description,
                        distance
                    )

                elif choice == "4":
                    try:
                        destination_id = int(
                            input("Destination ID to delete: ")
                        )

                        if destination_id <= 0:
                            print("Enter a valid destination ID.")
                            continue

                    except ValueError:
                        print("Enter a valid destination ID.")
                        continue

                    confirm = input(
                        "Delete this destination? (yes/no): "
                    ).strip().lower()

                    if confirm == "yes":
                        manager.delete_destination(destination_id)
                    else:
                        print("Delete cancelled.")

                elif choice == "0":
                    break

                else:
                    print("Invalid choice. Please try again.")

        finally:
            connection.close()

    def manage_packages(self):
        """Add, view and link packages to destinations."""

        connection = DatabaseConnection().get_connection()

        if connection is None:
            print("Database connection failed.")
            return

        manager = PackageManager(connection)
        destination_manager = DestinationManager(connection)

        try:
            while True:
                print("\n--- MANAGE PACKAGES ---")
                print("1. Add Package")
                print("2. View Packages")
                print("3. Link Destination")
                print("4. View Linked Destinations")
                print("0. Back to Admin Menu")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    name = input("Package name: ").strip()

                    if not name:
                        print("Package name is required.")
                        continue

                    print("\nSelect Package Type:")
                    print("1. Single Destination")
                    print("2. Multi Destination")

                    package_choice = input(
                        "Enter your choice: "
                    ).strip()

                    if package_choice == "1":
                        package_type = "Single Destination"
                    elif package_choice == "2":
                        package_type = "Multi Destination"
                    else:
                        print("Invalid package type.")
                        continue

                    try:
                        duration = int(input("Duration in days: "))
                        price = float(input("Base price (₹): "))

                        if duration <= 0 or price < 0:
                            print(
                                "Duration must be positive and "
                                "price cannot be negative."
                            )
                            continue

                    except ValueError:
                        print("Enter valid duration and price.")
                        continue

                    description = input("Description: ").strip()

                    if not description:
                        print("Description is required.")
                        continue

                    manager.add_package(
                        name,
                        package_type,
                        duration,
                        price,
                        description
                    )

                elif choice == "2":
                    manager.view_packages()

                elif choice == "3":
                    print("\nAvailable Packages:")
                    packages = manager.view_packages()

                    if not packages:
                        continue

                    print("\nAvailable Destinations:")
                    destinations = destination_manager.view_destinations()

                    if not destinations:
                        continue

                    try:
                        package_id = int(input("Package ID: "))
                        destination_id = int(input("Destination ID: "))
                        sequence_no = int(
                            input("Destination sequence number: ")
                        )

                        if (
                            package_id <= 0
                            or destination_id <= 0
                            or sequence_no <= 0
                        ):
                            print("IDs and sequence must be positive.")
                            continue

                        valid_package_ids = {
                            int(package["package_id"])
                            for package in packages
                        }

                        valid_destination_ids = {
                            int(destination["destination_id"])
                            for destination in destinations
                        }

                        if package_id not in valid_package_ids:
                            print("Package ID not found.")
                            continue

                        if destination_id not in valid_destination_ids:
                            print("Destination ID not found.")
                            continue

                    except (ValueError, KeyError):
                        print(
                            "Enter valid package, destination "
                            "and sequence values."
                        )
                        continue

                    manager.link_destination(
                        package_id,
                        destination_id,
                        sequence_no
                    )

                elif choice == "4":
                    packages = manager.view_packages()

                    if not packages:
                        continue

                    try:
                        package_id = int(
                            input(
                                "Enter Package ID to view destinations: "
                            )
                        )

                        valid_package_ids = {
                            int(package["package_id"])
                            for package in packages
                        }

                        if package_id not in valid_package_ids:
                            print("Package ID not found.")
                            continue

                    except (ValueError, KeyError):
                        print("Enter a valid Package ID.")
                        continue

                    manager.view_package_destinations(package_id)

                elif choice == "0":
                    break

                else:
                    print("Invalid choice. Please try again.")

        finally:
            connection.close()
