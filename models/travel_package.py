
class TravelPackage:
    """Represent a single or multi-destination package."""

    def __init__(
        self, package_name, package_type, duration_days, base_price
    ):
        self.package_name = package_name
        self.package_type = package_type
        self.duration_days = duration_days
        self.base_price = base_price

    def display_details(self):
        print(f"Package: {self.package_name}")
        print(f"Type: {self.package_type}")
        print(f"Duration: {self.duration_days} days")
        print(f"Base Price: ₹{self.base_price:.2f}")
