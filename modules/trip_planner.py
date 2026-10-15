
"""
Trip Planner
Displays a day-wise travel plan using existing packages
and their linked destinations.
"""

from mysql.connector import Error


class TripPlanner:
    """Plan a trip using an existing travel package."""

    def __init__(self, connection):
        self.connection = connection

    def plan_trip(self):
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
                    description
                FROM packages
                WHERE is_active = 1
                ORDER BY package_id
            """

            cursor.execute(query)
            packages = cursor.fetchall()

            if not packages:
                print("No active travel packages available.")
                return

            print("\n========== PLAN A TRIP ==========")

            for package in packages:
                print("-" * 40)
                print(f"Package ID : {package['package_id']}")
                print(f"Name       : {package['package_name']}")
                print(f"Type       : {package['package_type']}")
                print(f"Duration   : {package['duration_days']} days")
                print(f"Base Price : Rs. {float(package['base_price']):.2f}")

            print("-" * 40)

            try:
                package_id = int(input("Enter Package ID to plan your trip: "))
            except ValueError:
                print("Invalid input. Please enter a numeric Package ID.")
                return

            selected_package = next(
                (
                    package for package in packages
                    if package["package_id"] == package_id
                ),
                None
            )

            if selected_package is None:
                print("Invalid Package ID or inactive package.")
                return

            destination_query = """
                SELECT
                    d.destination_id,
                    d.name,
                    d.state,
                    d.description,
                    pd.sequence_no
                FROM package_destinations AS pd
                INNER JOIN destinations AS d
                    ON pd.destination_id = d.destination_id
                WHERE pd.package_id = %s
                ORDER BY pd.sequence_no
            """

            cursor.execute(destination_query, (package_id,))
            destinations = cursor.fetchall()

            print("\n========== YOUR TRIP PLAN ==========")
            print(f"Package    : {selected_package['package_name']}")
            print(f"Duration   : {selected_package['duration_days']} days")
            print(f"Base Price : Rs. {float(selected_package['base_price']):.2f}")

            if not destinations:
                print("\nNo destinations are linked to this package yet.")
                return

            duration = selected_package["duration_days"]
            print("\n--- DAY-WISE ITINERARY ---")

            for day in range(1, duration + 1):
                print(f"\nDay {day}:")

                if day <= len(destinations):
                    destination = destinations[day - 1]
                    print(
                        f"  Visit: {destination['name']}, "
                        f"{destination['state']}"
                    )
                    print(
                        f"  About: "
                        f"{destination['description'] or 'Details unavailable'}"
                    )
                else:
                    print("  Free time / local sightseeing.")

            print("\nTrip plan displayed successfully!")

        except Error as error:
            print(f"Database error while planning trip: {error}")

        finally:
            if cursor is not None:
                cursor.close()

