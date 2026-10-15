
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


class DatabaseSetup:
    """Create the database, tables, and default rate records."""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME", "indian_tourism_db")

    def create_database(self):
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{self.database}`"
            )
            print(f"Database '{self.database}' is ready.")
            return True

        except Error as error:
            print(f"Database setup error: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    def create_tables(self):
        """Create all project tables without deleting existing data."""

        tables = [
            """
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS travelers (
                traveler_id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(15) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS destinations (
                destination_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                description TEXT,
                estimated_distance_km DECIMAL(10,2) DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS packages (
                package_id INT AUTO_INCREMENT PRIMARY KEY,
                package_name VARCHAR(150) NOT NULL,
                package_type ENUM(
                    'Single Destination', 'Multi Destination'
                ) NOT NULL,
                duration_days INT NOT NULL,
                base_price DECIMAL(12,2) NOT NULL DEFAULT 0,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                CHECK (duration_days > 0),
                CHECK (base_price >= 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS package_destinations (
                package_destination_id INT AUTO_INCREMENT PRIMARY KEY,
                package_id INT NOT NULL,
                destination_id INT NOT NULL,
                sequence_no INT NOT NULL,
                FOREIGN KEY (package_id) REFERENCES packages(package_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (destination_id)
                    REFERENCES destinations(destination_id),
                UNIQUE (package_id, sequence_no),
                UNIQUE (package_id, destination_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS itinerary (
                itinerary_id INT AUTO_INCREMENT PRIMARY KEY,
                package_id INT NOT NULL,
                day_number INT NOT NULL,
                destination_id INT NOT NULL,
                activities TEXT,
                FOREIGN KEY (package_id) REFERENCES packages(package_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (destination_id)
                    REFERENCES destinations(destination_id),
                UNIQUE (package_id, day_number),
                CHECK (day_number > 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transport_rates (
                transport_rate_id INT AUTO_INCREMENT PRIMARY KEY,
                transport_type ENUM(
                    'Bus', 'Train', 'Own Car', 'Rental Car'
                ) NOT NULL,
                rate_per_km DECIMAL(10,2) NOT NULL DEFAULT 0,
                fixed_fare DECIMAL(10,2) NOT NULL DEFAULT 0,
                notes VARCHAR(255),
                CHECK (rate_per_km >= 0),
                CHECK (fixed_fare >= 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vehicle_settings (
                vehicle_setting_id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_type ENUM('Own Car', 'Rental Car') NOT NULL,
                mileage_km_per_litre DECIMAL(8,2) DEFAULT NULL,
                fuel_price_per_litre DECIMAL(8,2) DEFAULT NULL,
                daily_rental_cost DECIMAL(10,2) DEFAULT 0,
                CHECK (
                    mileage_km_per_litre IS NULL
                    OR mileage_km_per_litre > 0
                ),
                CHECK (
                    fuel_price_per_litre IS NULL
                    OR fuel_price_per_litre >= 0
                ),
                CHECK (daily_rental_cost >= 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS expense_rates (
                expense_rate_id INT AUTO_INCREMENT PRIMARY KEY,
                destination_id INT NOT NULL,
                expense_type ENUM(
                    'Accommodation', 'Food', 'Local Travel', 'Activities'
                ) NOT NULL,
                cost_per_person_per_day DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (destination_id)
                    REFERENCES destinations(destination_id),
                UNIQUE (destination_id, expense_type),
                CHECK (cost_per_person_per_day >= 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wishlists (
                wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
                traveler_id INT NOT NULL,
                destination_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (traveler_id) REFERENCES travelers(traveler_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (destination_id)
                    REFERENCES destinations(destination_id),
                UNIQUE (traveler_id, destination_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                traveler_id INT NOT NULL,
                package_id INT DEFAULT NULL,
                total_amount DECIMAL(12,2) NOT NULL,
                booking_status ENUM(
                    'Pending', 'Confirmed', 'Cancelled', 'Completed'
                ) DEFAULT 'Pending',
                start_date DATE DEFAULT NULL,
                travelers_count INT NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (traveler_id) REFERENCES travelers(traveler_id),
                FOREIGN KEY (package_id) REFERENCES packages(package_id),
                CHECK (total_amount >= 0),
                CHECK (travelers_count > 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS booking_destinations (
                booking_destination_id INT AUTO_INCREMENT PRIMARY KEY,
                booking_id INT NOT NULL,
                destination_id INT NOT NULL,
                visit_order INT NOT NULL,
                stay_days INT NOT NULL DEFAULT 1,
                FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (destination_id)
                    REFERENCES destinations(destination_id),
                UNIQUE (booking_id, visit_order),
                CHECK (visit_order > 0),
                CHECK (stay_days > 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS booking_expenses (
                booking_expense_id INT AUTO_INCREMENT PRIMARY KEY,
                booking_id INT NOT NULL,
                expense_type VARCHAR(50) NOT NULL,
                description VARCHAR(255),
                amount DECIMAL(12,2) NOT NULL,
                FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
                    ON DELETE CASCADE,
                CHECK (amount >= 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                booking_id INT NOT NULL,
                amount DECIMAL(12,2) NOT NULL DEFAULT 0,
                payment_status ENUM(
                    'Pending', 'Partially Paid', 'Paid'
                ) DEFAULT 'Pending',
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
                    ON DELETE CASCADE,
                CHECK (amount >= 0)
            )
            """
        ]

        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()

            for index, query in enumerate(tables, start=1):
                cursor.execute(query)
                print(f"Table {index}/14 ready.")

            connection.commit()
            print("All 14 tables are ready.")
            return True

        except Error as error:
            if connection is not None:
                connection.rollback()
            print(f"Table creation error: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    def seed_default_rates(self):
        """Insert default rates without duplicating existing expense rates."""

        connection = None
        cursor = None

        expense_rates = [
            (1, "Accommodation", 1500.00),
            (1, "Food", 500.00),
            (1, "Local Travel", 300.00),
            (1, "Activities", 400.00),
            (2, "Accommodation", 1200.00),
            (2, "Food", 400.00),
            (2, "Local Travel", 250.00),
            (2, "Activities", 350.00),
        ]

        transport_rates = [
            ("Bus", 0.00, 500.00, "Sample estimated fare per person"),
            ("Train", 0.00, 400.00, "Sample estimated fare per person"),
            ("Own Car", 8.00, 0.00, "Sample estimated cost per km"),
            ("Rental Car", 0.00, 2000.00, "Sample estimated daily rental"),
        ]

        vehicle_settings = [
            ("Own Car", 15.00, 105.00, 0.00),
            ("Rental Car", None, None, 2000.00),
        ]

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()

            # Confirm required destination IDs exist before adding rates.
            cursor.execute("""
                SELECT destination_id
                FROM destinations
                WHERE destination_id IN (1, 2)
            """)
            existing_ids = {row[0] for row in cursor.fetchall()}

            if not {1, 2}.issubset(existing_ids):
                print(
                    "Default rates not inserted: destination IDs 1 and 2 "
                    "must exist. Add the destinations first."
                )
                return False

            cursor.executemany("""
                INSERT INTO expense_rates
                    (destination_id, expense_type, cost_per_person_per_day)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    cost_per_person_per_day =
                    expense_rates.cost_per_person_per_day
            """, expense_rates)

            # Avoid duplicates in tables that do not have unique constraints
            # on transport_type or vehicle_type.
            for transport in transport_rates:
                cursor.execute("""
                    SELECT transport_rate_id
                    FROM transport_rates
                    WHERE transport_type = %s
                    LIMIT 1
                """, (transport[0],))

                if cursor.fetchone() is None:
                    cursor.execute("""
                        INSERT INTO transport_rates
                            (transport_type, rate_per_km, fixed_fare, notes)
                        VALUES (%s, %s, %s, %s)
                    """, transport)

            for vehicle in vehicle_settings:
                cursor.execute("""
                    SELECT vehicle_setting_id
                    FROM vehicle_settings
                    WHERE vehicle_type = %s
                    LIMIT 1
                """, (vehicle[0],))

                if cursor.fetchone() is None:
                    cursor.execute("""
                        INSERT INTO vehicle_settings
                            (vehicle_type, mileage_km_per_litre,
                             fuel_price_per_litre, daily_rental_cost)
                        VALUES (%s, %s, %s, %s)
                    """, vehicle)

            connection.commit()
            print("Default expense, transport, and vehicle rates are ready.")
            return True

        except Error as error:
            if connection is not None:
                connection.rollback()
            print(f"Default rate setup error: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    def setup(self):
        """Run database, table, and default-rate setup."""

        if not self.create_database():
            return False

        if not self.create_tables():
            return False

        if not self.seed_default_rates():
            return False

        return True


if __name__ == "__main__":
    setup = DatabaseSetup()

    if setup.setup():
        print("Database setup completed successfully.")
    else:
        print("Database setup failed. Check the error above.")
