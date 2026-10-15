
class BudgetCalculator:
    """Calculate an estimated trip budget."""

    def calculate_total(
        self, transport, accommodation, food, local_travel, activities
    ):
        costs = [
            transport,
            accommodation,
            food,
            local_travel,
            activities
        ]

        if any(cost < 0 for cost in costs):
            raise ValueError("Expenses cannot be negative.")

        return sum(costs)

    def display_breakdown(
        self, transport, accommodation, food, local_travel, activities
    ):
        print("\n--- TRIP BUDGET ---")
        print(f"Transport: ₹{transport:.2f}")
        print(f"Accommodation: ₹{accommodation:.2f}")
        print(f"Food: ₹{food:.2f}")
        print(f"Local Travel: ₹{local_travel:.2f}")
        print(f"Activities: ₹{activities:.2f}")

        total = self.calculate_total(
            transport, accommodation, food, local_travel, activities
        )
        print(f"Estimated Total: ₹{total:.2f}")
        return total
