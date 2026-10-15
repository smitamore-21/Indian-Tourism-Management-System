
class Reports:
    """Generate basic booking reports."""

    def __init__(self, connection):
        self.connection = connection

    def total_booking_revenue(self):
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
