
class WishlistManager:
    """Manage a traveler's wishlist."""

    def __init__(self, connection):
        self.connection = connection

    def add_to_wishlist(self, traveler_id, destination_id):
        if self.connection is None:
            print("Database connection unavailable.")
            return False

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO wishlists (traveler_id, destination_id)
                VALUES (%s, %s)
            """, (traveler_id, destination_id))

            self.connection.commit()
            print("Destination added to wishlist.")
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"Wishlist error: {error}")
            return False

        finally:
            cursor.close()
