
class Booking:
    """Represent a travel booking."""

    def __init__(
        self, traveler_id, package_id, total_amount, booking_status="Pending"
    ):
        self.traveler_id = traveler_id
        self.package_id = package_id
        self.total_amount = total_amount
        self.booking_status = booking_status

    def display_details(self):
        print(f"Traveler ID: {self.traveler_id}")
        print(f"Package ID: {self.package_id}")
        print(f"Total Amount: ₹{self.total_amount:.2f}")
        print(f"Booking Status: {self.booking_status}")
