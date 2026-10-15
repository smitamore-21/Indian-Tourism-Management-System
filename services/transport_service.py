
class TransportService:
    """Estimate transport costs."""

    def calculate_car_fuel_cost(self, distance_km, mileage, fuel_price):
        if distance_km < 0 or mileage <= 0 or fuel_price < 0:
            raise ValueError("Invalid distance, mileage, or fuel price.")

        return (distance_km / mileage) * fuel_price

    def calculate_rental_cost(self, days, daily_rent):
        if days < 0 or daily_rent < 0:
            raise ValueError("Days and rental cost cannot be negative.")

        return days * daily_rent
