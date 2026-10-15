
class ItineraryPlanner:
    """Build a simple multi-destination itinerary."""

    def create_itinerary(self, destinations):
        if not destinations:
            print("Please add at least one destination.")
            return []

        itinerary = []

        for day, destination in enumerate(destinations, start=1):
            item = {
                "day": day,
                "destination": destination
            }
            itinerary.append(item)

        return itinerary

    def display_itinerary(self, itinerary):
        print("\n--- YOUR TRIP ITINERARY ---")

        for item in itinerary:
            print(
                f"Day {item['day']}: {item['destination']}"
            )
