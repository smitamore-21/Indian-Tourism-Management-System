
from database.connection import DatabaseConnection
from modules.destination_manager import DestinationManager


def main():
    connection = DatabaseConnection().get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    manager = DestinationManager(connection)

    try:
        print("\n--- DESTINATION TEST MENU ---")
        print("1. Add Destination")
        print("2. View Destinations")
        print("3. Update Destination")
        print("4. Delete Destination")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Destination name: ").strip()
            state = input("State: ").strip()
            description = input("Description: ").strip()

            try:
                distance = float(input("Distance in km: "))
                if distance < 0:
                    print("Distance cannot be negative.")
                    return
            except ValueError:
                print("Enter a valid distance.")
                return

            manager.add_destination(
                name, state, description, distance
            )

        elif choice == "2":
            manager.view_destinations()

        elif choice == "3":
            try:
                destination_id = int(input("Destination ID: "))
                distance = float(input("Updated distance in km: "))

                if destination_id <= 0 or distance < 0:
                    print("Enter a valid ID and distance.")
                    return
            except ValueError:
                print("Enter valid numeric values.")
                return

            name = input("Updated name: ").strip()
            state = input("Updated state: ").strip()
            description = input("Updated description: ").strip()

            manager.update_destination(
                destination_id, name, state, description, distance
            )

        elif choice == "4":
            try:
                destination_id = int(input("Destination ID to delete: "))
                if destination_id <= 0:
                    print("Enter a valid ID.")
                    return
            except ValueError:
                print("Enter a valid destination ID.")
                return

            confirm = input(
                "Are you sure you want to delete it? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                manager.delete_destination(destination_id)
            else:
                print("Delete cancelled.")

        elif choice == "0":
            print("Test completed.")

        else:
            print("Invalid choice.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
