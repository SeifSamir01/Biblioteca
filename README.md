# Biblioteca

A comprehensive library management system built with Python, PyQt5, and SQLite3. The system provides a user-friendly interface for library users to manage book borrowing, returns, and fines.

## Features

- **User Management**
  - Registration with email, national ID, and basic info validation
  - Secure login system with session management
  - Personal dashboard with user information

- **Book Management**
  - Browse available books with real-time quantity tracking
  - Search functionality by book title
  - Book rating system (1-5 stars)
  - Average rating display for each book

- **Borrowing System**
  - Borrow books with automatic due date assignment (14 days)
  - View borrowed books with status tracking
  - Automatic overdue status updates
  - One copy per book per user limit

- **Fine Management**
  - View assigned fines
  - Fine payment processing
  - Status tracking (Paid/Unpaid)

## Technology Stack

- Python 3.12.8
- PyQt5 for GUI
- SQLite3 for database
- Object-Oriented Programming paradigm

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install PyQt5
```

3. Initialize database:
```bash
sqlite3 library.db < ddl.sql
```

## Project Structure

```
library_management/
├── main.py           # Application entry point
├── session.py        # User session management
├── first_page.py     # Welcome page
├── login_page.py     # Login interface
├── register_page.py  # Registration interface
├── homePage.py       # User dashboard
├── tap_page.py       # Tab container
├── books.py          # Book management
├── borrowing.py      # Borrowing system
├── fines.py          # Fine management
├── ddl.sql          # Database schema and tables creation
└── ERD and Schema.pdf # Database design documentation
```

## Running the Application

```bash
python main.py
```

## Security Features

- Password validation (minimum 6 characters)
- National ID validation (14 characters)
- Duplicate user prevention
- Session management for user state

## Usage Requirements

- Python 3.6+
- PyQt5
- SQLite3
- 1200x800 minimum screen resolution

## Limitations

- Administrator interface not implemented
- No password recovery system
- Fixed 14-day borrowing period
- No standardized fining policy - fine amounts are manually set by administrators
