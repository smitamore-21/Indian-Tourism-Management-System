
class Destination:
    """Represent a tourist destination."""

    def __init__(self, name, state, description):
        self.name = name
        self.state = state
        self.description = description

    def display_details(self):
        print(f"Destination: {self.name}")
        print(f"State: {self.state}")
        print(f"Description: {self.description}")
