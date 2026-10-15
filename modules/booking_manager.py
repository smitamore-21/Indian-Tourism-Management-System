
class BookingManager:
    """Manage traveler bookings."""

    def __init__(self, connection):
        self.connection = connection

    def view_traveler_bookings(self, traveler_id):
        if self.connection is None:
            print("Database connection unavailable.")
            return []

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT booking_id, total_amount, booking_status
                FROM bookings
                WHERE traveler_id = %s
                ORDER BY booking_id DESC
            """, (traveler_id,))

            bookings = cursor.fetchall()

            if bookings:
                print("\n--- MY BOOKINGS ---")
                for booking in bookings:
                    print(
                        f"Booking ID: {booking[0]} | "
                        f"Amount: Rs. {booking[1]} | "
                        f"Status: {booking[2]}"
                    )

            return bookings

        except Exception as error:
            print(f"Error fetching bookings: {error}")
            return []

        finally:
            cursor.close()

    def create_booking(self, traveler_id):
        if self.connection is None:
            print("Database connection unavailable.")
            return False

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT package_id, package_name, duration_days, base_price
                FROM packages
                WHERE is_active = 1
                ORDER BY package_id
            """)
            packages = cursor.fetchall()

            if not packages:
                print("No active packages available.")
                return False

            print("\n--- AVAILABLE PACKAGES ---")
            for package in packages:
                print(
                    f"ID: {package[0]} | {package[1]} | "
                    f"{package[2]} days | Rs. {package[3]}"
                )

            try:
                package_id = int(input("Enter package ID to book: ").strip())
                travelers_count = int(
                    input("Enter number of travelers: ").strip()
                )
            except ValueError:
                print("Please enter valid numeric values.")
                return False

            if travelers_count <= 0:
                print("Number of travelers must be greater than zero.")
                return False

            selected_package = next(
                (package for package in packages if package[0] == package_id),
                None
            )

            if selected_package is None:
                print("Invalid package ID.")
                return False

            total_amount = selected_package[3] * travelers_count

            confirm = input(
                f"Confirm booking for {selected_package[1]} "
                f"for {travelers_count} traveler(s), "
                f"total Rs. {total_amount}? (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Booking cancelled.")
                return False

            cursor.execute("""
                INSERT INTO bookings
                    (traveler_id, package_id, total_amount,
                     booking_status, travelers_count)
                VALUES (%s, %s, %s, 'Pending', %s)
            """, (
                traveler_id,
                package_id,
                total_amount,
                travelers_count
            ))

            booking_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO payments
                    (booking_id, amount, payment_status)
                VALUES (%s, %s, 'Pending')
            """, (booking_id, 0))

            self.connection.commit()

            print("\nBooking created successfully!")
            print(f"Booking ID: {booking_id}")
            print(f"Package: {selected_package[1]}")
            print(f"Total Amount: Rs. {total_amount}")
            print("Booking Status: Pending")
            

            return True

        except Exception as error:
            self.connection.rollback()
            print(f"Booking creation error: {error}")
            return False

        finally:
            cursor.close()
