import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime, date, timedelta # Import timedelta for date calculations

# Database Configuration
DB_CONFIG = {
    'user': 'root',
    'password': '1',
    'host': 'localhost', # e.g., 'localhost'
    'database': 'LMS'
}

# Late Fee Configuration
DAILY_LATE_FEE = 0.25 # $0.25 per day late

# Database Connection Function
def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
        return None

# GUI Implementation
class LMSApp:
    def __init__(self, root):
        self.root = root
        root.title("Library Management System")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Create Tabs
        self.create_checkout_tab()
        self.create_add_borrower_tab()
        self.create_add_book_tab()
        self.create_loaned_copies_tab()
        self.create_late_returns_tab()
        self.create_borrower_late_fees_tab()
        self.create_borrower_book_late_fees_tab()