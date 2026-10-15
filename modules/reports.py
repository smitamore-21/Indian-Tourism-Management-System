
class Reports:
    """Generate booking and revenue reports."""

    def __init__(self, connection):
        self.connection = connection

    def total_booking_revenue(self):
        """Calculate total value of confirmed bookings."""

        if self.connection is None:
            print("Database connection unavailable.")
            return 0

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0)
                FROM bookings
                WHERE booking_status = 'Confirmed'
            """)

            result = cursor.fetchone()
            total = result[0] if result else 0

            print(f"Confirmed booking value: ₹{total:.2f}")
            return total

        except Exception as error:
            print(f"Report error: {error}")
            return 0

        finally:
            cursor.close()

    def package_booking_count(self):
        """Display only packages that have bookings."""

        if self.connection is None:
            print("Database connection unavailable.")
            return

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    p.package_id,
                    p.package_name,
                    COUNT(b.booking_id) AS total_bookings,
                    COALESCE(SUM(b.travelers_count), 0) AS total_travelers
                FROM packages p
                INNER JOIN bookings b
                    ON p.package_id = b.package_id
                GROUP BY p.package_id, p.package_name
                ORDER BY total_bookings DESC, p.package_name
            """)

            rows = cursor.fetchall()

            print("\n========== PACKAGE BOOKING REPORT ==========")

            if not rows:
                print("No bookings found.")
                return

            print("-" * 90)

            for row in rows:
                print(f"Package ID     : {row[0]}")
                print(f"Package Name   : {row[1]}")
                print(f"Total Bookings : {row[2]}")
                print(f"Total Travelers: {row[3]}")
                print("-" * 90)

        except Exception as error:
            print(f"Report error: {error}")

        finally:
            cursor.close()
