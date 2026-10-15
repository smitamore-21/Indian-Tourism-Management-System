
class Payment:
    """Represent a booking payment record."""

    VALID_STATUSES = ("Pending", "Partially Paid", "Paid")

    def __init__(
        self, booking_id, amount, payment_status="Pending"
    ):
        if payment_status not in self.VALID_STATUSES:
            raise ValueError("Invalid payment status.")

        if amount < 0:
            raise ValueError("Payment amount cannot be negative.")

        self.booking_id = booking_id
        self.amount = amount
        self.payment_status = payment_status

    def display_details(self):
        print(f"Booking ID: {self.booking_id}")
        print(f"Amount: ₹{self.amount:.2f}")
        print(f"Payment Status: {self.payment_status}")
