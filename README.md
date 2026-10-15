# 🇮🇳 Indian Tourism Management System

A Python and MySQL-based console application that helps travelers explore destinations, select travel packages, plan itineraries, estimate trip budgets, manage bookings, and track payments.

## 📌 Project Overview

The Indian Tourism Management System is designed to simplify travel planning across India. It provides separate functionalities for administrators and travelers, with MySQL used to store application data.

## ✨ Features

- **Admin Login:** Access administrative functions.
- **Traveler Registration & Login:** Register and securely access a traveler account.
- **Destination Management:** Manage tourist destinations.
- **Travel Packages:** Browse single-destination and multi-destination packages.
- **Trip Planner:** Plan trips and itineraries.
- **Budget Calculator:** Estimate travel expenses.
- **Transport Options:** Support for bus, train, own car, and rental car.
- **Booking Management:** Manage traveler bookings.
- **Wishlist:** Save preferred destinations.
- **Payment Tracking:** Track payment status.
- **Reports:** View booking-related reports.

## 🛠️ Technologies Used

- Python
- Object-Oriented Programming (OOP)
- MySQL
- MySQL Connector for Python
- python-dotenv
- Git and GitHub

## 📂 Project Structure

```text
Indian-Tourism-Management-System/
├── database/
│   ├── connection.py
│   └── setup_database.py
├── models/
├── modules/
├── services/
├── utils/
├── main.py
├── requirements.txt
├── test_destinations.py
├── test_packages.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/smitamore-21/Indian-Tourism-Management-System.git
cd Indian-Tourism-Management-System
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=indian_tourism_db
```

Replace `your_mysql_password` with your local MySQL password.

**Security:** Never upload your `.env` file or database password to GitHub.

### 5. Set up the database

Ensure MySQL Server is running. Then run:

```bash
python3 -c "from database.setup_database import DatabaseSetup; print(DatabaseSetup().setup())"
```

Run the setup command only after reviewing your database configuration. It creates the database and tables if they do not exist and inserts default rate records. Ensure your database user has the required permissions.

### 6. Run the application

```bash
python3 main.py
```

## 🧪 Testing

Run the available test scripts:

```bash
python3 test_destinations.py
python3 test_packages.py
```

## 🔐 Security Notes

- Store credentials in environment variables.
- Keep `.env` out of version control.
- Use password hashing for user authentication.

## 🚀 Future Improvements

- Add a graphical user interface or web interface.
- Integrate live travel and transport information.
- Add online payment gateway integration.
- Improve automated testing and reporting.

## 👩‍💻 Author

**Smita More**

GitHub: [smitamore-21](https://github.com/smitamore-21)

## 📄 Project Status

Under development.
