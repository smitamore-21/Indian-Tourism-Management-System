
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from the project's .env file
load_dotenv()


class DatabaseConnection:
    """Manage MySQL database connections."""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv(
            "DB_NAME", "indian_tourism_db"
        )

    def get_connection(self):
        """Create and return a MySQL connection."""

        if not self.password:
            print("Database password is missing in .env file.")
            return None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                return connection

        except Error as error:
            print(f"Database connection error: {error}")

        return None
