class PaymentManager:
    """Manage and display payment records."""

    def __init__(self, connection):
        self.connection = connection

    def view_payment_status(self, booking_id):
        if self.connection is None:
            print("Database connection unavailable.")
            return []

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT payment_id, amount, payment_status
                FROM payments
                WHERE booking_id = %s
                ORDER BY payment_id DESC
            """, (booking_id,))

            payments = cursor.fetchall()

            if not payments:
                print("No payment records found for this booking.")
                return []

            print("\n--- PAYMENT DETAILS ---")
            for payment in payments:
                print(f"Payment ID: {payment[0]}")
                print(f"Payment Amount: Rs. {payment[1]:,.2f}")
                print(f"Payment Status: {payment[2]}")
                print("-" * 30)

            return payments

        except Exception as error:
            print(f"Payment lookup error: {error}")
            return []

        finally:
            cursor.close()

    def mark_payment_as_paid(self, booking_id):
        if self.connection is None:
            print("Database connection unavailable.")
            return False

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT total_amount
                FROM bookings
                WHERE booking_id = %s
            """, (booking_id,))

            booking = cursor.fetchone()

            if not booking:
                print("Booking not found.")
                return False

            total_amount = booking[0]

            cursor.execute("""
                SELECT payment_id, payment_status
                FROM payments
                WHERE booking_id = %s
                ORDER BY payment_id DESC
                LIMIT 1
            """, (booking_id,))

            payment = cursor.fetchone()

            if not payment:
                print("No payment record found for this booking.")
                return False

            if payment[1] == "Paid":
                print("This booking is already marked as Paid.")
                return False

            confirm = input(
                f"Mark Rs. {total_amount:,.2f} as paid? (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Payment update cancelled.")
                return False

            cursor.execute("""
                UPDATE payments
                SET amount = %s, payment_status = 'Paid'
                WHERE payment_id = %s
            """, (total_amount, payment[0]))

            self.connection.commit()
            print("Payment status updated to Paid.")
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"Payment update error: {error}")
            return False

        finally:
            cursor.close()