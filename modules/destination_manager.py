
"""
Destination Manager
Handles CRUD operations for tourist destinations.
"""


class DestinationManager:
    """Manage tourist destinations using MySQL."""

    def __init__(self, connection):
        self.connection = connection

    def add_destination(self, name, state, description, distance):
        """Add a new tourist destination."""

        if self.connection is None:
            print("Database connection unavailable.")
            return False

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                INSERT INTO destinations
                (name, state, description, estimated_distance_km)
                VALUES (%s, %s, %s, %s)
            """

            values = (name, state, description, distance)

            cursor.execute(query, values)
            self.connection.commit()

            print("Destination added successfully!")
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"Error adding destination: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def view_destinations(self):
        """Display all destinations and return dictionaries."""

        if self.connection is None:
            print("Database connection unavailable.")
            return []

        cursor = None

        try:
            # Dictionary cursor fixes the tuple/dictionary mismatch.
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT
                    destination_id,
                    name,
                    state,
                    description,
                    estimated_distance_km
                FROM destinations
                ORDER BY destination_id
            """

            cursor.execute(query)
            destinations = cursor.fetchall()

            if not destinations:
                print("No destinations found.")
                return []

            print("\n--- TOURIST DESTINATIONS ---")

            for place in destinations:
                print("-" * 40)
                print(f"ID: {place['destination_id']}")
                print(f"Name: {place['name']}")
                print(f"State: {place['state']}")
                print(f"Description: {place['description']}")
                print(
                    f"Distance: "
                    f"{place['estimated_distance_km']} km"
                )

            print("-" * 40)

            return destinations

        except Exception as error:
            print(f"Error viewing destinations: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

    def update_destination(
        self,
        destination_id,
        name,
        state,
        description,
        distance
    ):
        """Update an existing tourist destination."""

        if self.connection is None:
            print("Database connection unavailable.")
            return False

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                UPDATE destinations
                SET
                    name = %s,
                    state = %s,
                    description = %s,
                    estimated_distance_km = %s
                WHERE destination_id = %s
            """

            values = (
                name,
                state,
                description,
                distance,
                destination_id
            )

            cursor.execute(query, values)

            if cursor.rowcount == 0:
                print(
                    "Destination not found or no changes were made."
                )
                return False

            self.connection.commit()
            print("Destination updated successfully!")
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"Error updating destination: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def delete_destination(self, destination_id):
        """Delete a tourist destination."""

        if self.connection is None:
            print("Database connection unavailable.")
            return False

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                DELETE FROM destinations
                WHERE destination_id = %s
            """

            cursor.execute(query, (destination_id,))

            if cursor.rowcount == 0:
                print("Destination not found.")
                return False

            self.connection.commit()
            print("Destination deleted successfully!")
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"Error deleting destination: {error}")
            print(
                "This destination may be linked to a package, "
                "booking or itinerary."
            )
            return False

        finally:
            if cursor is not None:
                cursor.close()
