
from decimal import Decimal, InvalidOperation


class BudgetCalculator:
    """Calculate an estimated trip budget using database rates."""

    def __init__(self, connection):
        self.connection = connection

    def calculate_budget(self):
        cursor = None

        try:
            cursor = self.connection.cursor(dictionary=True)

            # Show destinations available for budget calculation.
            cursor.execute("""
                SELECT destination_id, name, state
                FROM destinations
                ORDER BY destination_id
            """)
            destinations = cursor.fetchall()

            if not destinations:
                print("No destinations available.")
                return

            print("\n--- AVAILABLE DESTINATIONS ---")
            for destination in destinations:
                print(
                    f"{destination['destination_id']}. "
                    f"{destination['name']}, {destination['state']}"
                )

            try:
                destination_id = int(input("Enter destination ID: "))
                days = int(input("Enter number of days: "))
                people = int(input("Enter number of travelers: "))
            except ValueError:
                print("Please enter valid whole numbers.")
                return

            if days <= 0 or people <= 0:
                print("Days and travelers must be greater than zero.")
                return

            selected = next(
                (
                    destination for destination in destinations
                    if destination["destination_id"] == destination_id
                ),
                None
            )

            if selected is None:
                print("Invalid destination ID.")
                return

            cursor.execute("""
                SELECT expense_type, cost_per_person_per_day
                FROM expense_rates
                WHERE destination_id = %s
            """, (destination_id,))
            rates = cursor.fetchall()

            if not rates:
                print("No expense rates configured for this destination.")
                return

            expense_total = Decimal("0.00")
            print("\n--- ESTIMATED EXPENSE BREAKDOWN ---")

            for rate in rates:
                amount = (
                    Decimal(str(rate["cost_per_person_per_day"]))
                    * days
                    * people
                )
                expense_total += amount
                print(f"{rate['expense_type']}: Rs. {amount:.2f}")

            # Show available transport types.
            cursor.execute("""
                SELECT transport_type, rate_per_km, fixed_fare, notes
                FROM transport_rates
                ORDER BY transport_rate_id
            """)
            transport_options = cursor.fetchall()

            if not transport_options:
                print("No transport rates configured.")
                return

            print("\n--- TRANSPORT OPTIONS ---")
            for index, transport in enumerate(transport_options, start=1):
                print(
                    f"{index}. {transport['transport_type']} "
                    f"(fixed fare: Rs. {transport['fixed_fare']}, "
                    f"rate/km: Rs. {transport['rate_per_km']})"
                )

            try:
                transport_choice = int(input("Choose transport option: "))
            except ValueError:
                print("Please enter a valid transport option.")
                return

            if not 1 <= transport_choice <= len(transport_options):
                print("Invalid transport option.")
                return

            transport = transport_options[transport_choice - 1]
            transport_type = transport["transport_type"]

            transport_cost = Decimal("0.00")

            if transport_type in ("Bus", "Train"):
                transport_cost = (
                    Decimal(str(transport["fixed_fare"])) * people
                )

            elif transport_type == "Own Car":
                try:
                    distance = Decimal(
                        input("Enter total trip distance in km: ").strip()
                    )
                    if distance <= 0:
                        print("Distance must be greater than zero.")
                        return
                except (InvalidOperation, ValueError):
                    print("Enter a valid distance.")
                    return

                cursor.execute("""
                    SELECT mileage_km_per_litre, fuel_price_per_litre
                    FROM vehicle_settings
                    WHERE vehicle_type = 'Own Car'
                    ORDER BY vehicle_setting_id
                    LIMIT 1
                """)
                vehicle = cursor.fetchone()

                if (
                    vehicle is None
                    or vehicle["mileage_km_per_litre"] is None
                    or vehicle["mileage_km_per_litre"] <= 0
                    or vehicle["fuel_price_per_litre"] is None
                ):
                    print("Own car mileage or fuel price is not configured.")
                    return

                mileage = Decimal(str(vehicle["mileage_km_per_litre"]))
                fuel_price = Decimal(str(vehicle["fuel_price_per_litre"]))
                transport_cost = distance / mileage * fuel_price

            elif transport_type == "Rental Car":
                try:
                    distance = Decimal(
                        input("Enter total trip distance in km: ").strip()
                    )
                    if distance <= 0:
                        print("Distance must be greater than zero.")
                        return
                except (InvalidOperation, ValueError):
                    print("Enter a valid distance.")
                    return

                cursor.execute("""
                    SELECT daily_rental_cost
                    FROM vehicle_settings
                    WHERE vehicle_type = 'Rental Car'
                    ORDER BY vehicle_setting_id
                    LIMIT 1
                """)
                vehicle = cursor.fetchone()

                if vehicle is None:
                    print("Rental car settings are not configured.")
                    return

                daily_rent = Decimal(
                    str(vehicle["daily_rental_cost"] or 0)
                )
                per_km = Decimal(str(transport["rate_per_km"]))
                transport_cost = daily_rent * days + per_km * distance

            total = expense_total + transport_cost

            print("\n========== BUDGET SUMMARY ==========")
            print(f"Destination : {selected['name']}")
            print(f"Duration    : {days} day(s)")
            print(f"Travelers   : {people}")
            print(f"Expenses    : Rs. {expense_total:.2f}")
            print(f"Transport   : Rs. {transport_cost:.2f}")
            print("------------------------------------")
            print(f"Estimated Total: Rs. {total:.2f}")
            print("Note: This is an estimate based on configured sample rates.")

        except Exception as error:
            print(f"Budget calculation error: {error}")

        finally:
            if cursor is not None:
                cursor.close()
