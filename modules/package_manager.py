
"""
Package Manager
Handles travel package CRUD operations and destination linking.
"""

from mysql.connector import Error


class PackageManager:
    """Manage tourism packages in the database."""

    def __init__(self, connection):
        self.connection = connection

    def add_package(
        self,
        name,
        package_type,
        duration,
        price,
        description
    ):
        """Add a new travel package."""

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                INSERT INTO packages
                (
                    package_name,
                    package_type,
                    duration_days,
                    base_price,
                    description
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                name,
                package_type,
                duration,
                price,
                description
            )

            cursor.execute(query, values)
            self.connection.commit()

            print("Package added successfully!")
            return True

        except Error as error:
            self.connection.rollback()
            print(f"Error adding package: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def view_packages(self):
        """Display all travel packages."""

        cursor = None

        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT
                    package_id,
                    package_name,
                    package_type,
                    duration_days,
                    base_price,
                    description,
                    is_active
                FROM packages
                ORDER BY package_id
            """

            cursor.execute(query)
            packages = cursor.fetchall()

            if not packages:
                print("No packages found.")
                return []

            print("\n========== TRAVEL PACKAGES ==========")

            for package in packages:
                print("-" * 40)
                print(f"Package ID : {package['package_id']}")
                print(f"Name       : {package['package_name']}")
                print(f"Type       : {package['package_type']}")
                print(f"Duration   : {package['duration_days']} days")
                print(
                    f"Base Price : Rs. "
                    f"{float(package['base_price']):.2f}"
                )
                print(
                    f"Description: "
                    f"{package['description'] or 'N/A'}"
                )
                print(f"Active     : {package['is_active']}")

            print("-" * 40)

            return packages

        except Error as error:
            print(f"Error viewing packages: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

    def link_destination(
        self,
        package_id,
        destination_id,
        sequence_no
    ):
        """Link a destination to a travel package."""

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                INSERT INTO package_destinations
                (
                    package_id,
                    destination_id,
                    sequence_no
                )
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    sequence_no = VALUES(sequence_no)
            """

            values = (
                package_id,
                destination_id,
                sequence_no
            )

            cursor.execute(query, values)
            self.connection.commit()

            print("Destination linked to package successfully!")
            return True

        except Error as error:
            self.connection.rollback()
            print(f"Error linking destination: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def view_package_destinations(self, package_id):
        """Display destinations linked to a package."""

        cursor = None

        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT
                    d.destination_id,
                    d.name,
                    d.state,
                    pd.sequence_no
                FROM package_destinations AS pd
                INNER JOIN destinations AS d
                    ON pd.destination_id = d.destination_id
                WHERE pd.package_id = %s
                ORDER BY pd.sequence_no
            """

            cursor.execute(query, (package_id,))
            destinations = cursor.fetchall()

            if not destinations:
                print("No destinations linked to this package.")
                return []

            print("\n--- PACKAGE DESTINATIONS ---")

            for destination in destinations:
                print(
                    f"Stop {destination['sequence_no']}: "
                    f"{destination['name']}, "
                    f"{destination['state']} "
                    f"(ID: {destination['destination_id']})"
                )

            return destinations

        except Error as error:
            print(f"Error viewing package destinations: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()
