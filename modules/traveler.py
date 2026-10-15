from database.connection import DatabaseConnection
from modules.package_manager import PackageManager
from modules.destination_manager import DestinationManager
from modules.trip_planner import TripPlanner
from modules.budget_calculator import BudgetCalculator
from modules.booking_manager import BookingManager
from modules.wishlist_manager import WishlistManager
from modules.payment_manager import PaymentManager


class TravelerDashboard:
    """Display and handle traveler options."""

    def __init__(self, traveler_id=None, traveler_name="Traveler"):
        self.traveler_id = traveler_id
        self.traveler_name = traveler_name

    def display_menu(self):
        while True:
            print(f"\n--- TRAVELER DASHBOARD: {self.traveler_name} ---")
            print("1. Browse Destinations")
            print("2. Browse Packages")
            print("3. Plan a Trip")
            print("4. Calculate Budget")
            print("5. Manage Wishlist")
            print("6. Create Booking")
            print("7. My Bookings")
            print("8. Payment Status")
            print("9. Update Payment Status")
            print("0. Logout")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.browse_destinations()
            elif choice == "2":
                self.browse_packages()
            elif choice == "3":
                self.run_trip_planner()
            elif choice == "4":
                self.run_budget_calculator()
            elif choice == "5":
                self.manage_wishlist()
            elif choice == "6":
                self.create_booking()
            elif choice == "7":
                self.view_bookings()
            elif choice == "8":
                self.view_payment_status()
            elif choice == "9":
                self.update_payment_status()
            elif choice == "0":
                print("Traveler logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")

    def browse_destinations(self):
        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return
        try:
            DestinationManager(connection).view_destinations()
        except Exception as error:
            print(f"Error browsing destinations: {error}")
        finally:
            connection.close()

    def browse_packages(self):
        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return
        try:
            PackageManager(connection).view_packages()
        except Exception as error:
            print(f"Error browsing packages: {error}")
        finally:
            connection.close()

    def run_trip_planner(self):
        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return
        try:
            TripPlanner(connection).plan_trip()
        except Exception as error:
            print(f"Trip planner error: {error}")
        finally:
            connection.close()

    def run_budget_calculator(self):
        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return
        try:
            BudgetCalculator(connection).calculate_budget()
        except Exception as error:
            print(f"Budget calculator error: {error}")
        finally:
            connection.close()

    def manage_wishlist(self):
        if self.traveler_id is None:
            print("Traveler login required to manage wishlist.")
            return

        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            manager = WishlistManager(connection)

            while True:
                print("\n--- MANAGE WISHLIST ---")
                print("1. View Destinations")
                print("2. Add Destination to Wishlist")
                print("3. View My Wishlist")
                print("0. Back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    cursor = connection.cursor()
                    try:
                        cursor.execute("""
                            SELECT destination_id, name, state
                            FROM destinations
                            ORDER BY destination_id
                        """)
                        destinations = cursor.fetchall()
                        if destinations:
                            for destination in destinations:
                                print(destination)
                        else:
                            print("No destinations found.")
                    finally:
                        cursor.close()

                elif choice == "2":
                    try:
                        destination_id = int(
                            input("Enter destination ID: ").strip()
                        )
                        manager.add_to_wishlist(
                            self.traveler_id, destination_id
                        )
                    except ValueError:
                        print("Please enter a valid destination ID.")

                elif choice == "3":
                    cursor = connection.cursor()
                    try:
                        cursor.execute("""
                            SELECT d.destination_id, d.name, d.state,
                                   w.created_at
                            FROM wishlists AS w
                            JOIN destinations AS d
                                ON w.destination_id = d.destination_id
                            WHERE w.traveler_id = %s
                            ORDER BY w.created_at DESC
                        """, (self.traveler_id,))
                        wishlist = cursor.fetchall()

                        if wishlist:
                            print("\n--- MY WISHLIST ---")
                            for item in wishlist:
                                print(item)
                        else:
                            print("Your wishlist is empty.")
                    finally:
                        cursor.close()

                elif choice == "0":
                    break
                else:
                    print("Invalid choice.")

        except Exception as error:
            print(f"Wishlist error: {error}")
        finally:
            connection.close()

    def create_booking(self):
        if self.traveler_id is None:
            print("Traveler login required to create a booking.")
            return

        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            BookingManager(connection).create_booking(self.traveler_id)
        except Exception as error:
            print(f"Booking creation error: {error}")
        finally:
            connection.close()

    def view_bookings(self):
        if self.traveler_id is None:
            print("Traveler login required to view bookings.")
            return

        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            bookings = BookingManager(
                connection
            ).view_traveler_bookings(self.traveler_id)

            if not bookings:
                print("No bookings found.")
        except Exception as error:
            print(f"Booking error: {error}")
        finally:
            connection.close()

    def view_payment_status(self):
        if self.traveler_id is None:
            print("Traveler login required to view payment status.")
            return

        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            bookings = BookingManager(
                connection
            ).view_traveler_bookings(self.traveler_id)

            if not bookings:
                print("No bookings found. Create a booking first.")
                return

            try:
                booking_id = int(
                    input("Enter booking ID to check payment: ").strip()
                )
            except ValueError:
                print("Please enter a valid booking ID.")
                return

            if not any(b[0] == booking_id for b in bookings):
                print("Invalid booking ID for your account.")
                return

            PaymentManager(connection).view_payment_status(booking_id)

        except Exception as error:
            print(f"Payment status error: {error}")
        finally:
            connection.close()

    def update_payment_status(self):
        if self.traveler_id is None:
            print("Traveler login required to update payment.")
            return

        connection = DatabaseConnection().get_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            bookings = BookingManager(
                connection
            ).view_traveler_bookings(self.traveler_id)

            if not bookings:
                print("No bookings found.")
                return

            try:
                booking_id = int(
                    input("Enter booking ID to update payment: ").strip()
                )
            except ValueError:
                print("Please enter a valid booking ID.")
                return

            if not any(b[0] == booking_id for b in bookings):
                print("Invalid booking ID for your account.")
                return

            PaymentManager(connection).mark_payment_as_paid(booking_id)

        except Exception as error:
            print(f"Payment update error: {error}")
        finally:
            connection.close()