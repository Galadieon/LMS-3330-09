import os
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

# --- Requirement 1: Checkout Book ---
def checkout_book(book_id, branch_id, card_no):
    """Handles the book checkout process."""
    conn = get_db_connection()
    if not conn:
        return "", ""

    cursor = conn.cursor()
    result_text = ""
    sql_query_executed = ""

    try:
        # Calculate due date as 31 days from date_out (current date)
        date_out = date.today()
        due_date = date_out + timedelta(days=31)

        # SQL Query: Insert into Book_Loans
        sql_query = """
        INSERT INTO Book_Loans (book_id, branch_id, card_no, date_out, due_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        sql_query_executed = sql_query.strip() # Store the query string
        cursor.execute(sql_query, (book_id, branch_id, card_no, date_out, due_date))
        conn.commit()

        result_text += "Book checked out successfully.\n"

        # After successful insert, query Book_Copies to show updated count
        # This assumes the trigger has fired and updated the count
        sql_check_copies = """
        SELECT no_of_copies
        FROM Book_Copies
        WHERE book_id = %s AND branch_id = %s
        """
        cursor.execute(sql_check_copies, (book_id, branch_id))
        updated_copies = cursor.fetchone()

        if updated_copies:
            result_text += f"Updated copies for Book ID {book_id} at Branch ID {branch_id}: {updated_copies[0]}"
        else:
            result_text += f"Could not retrieve updated copies for Book ID {book_id} at Branch ID {branch_id}. (Trigger might not have updated yet or issue with query)"

    except mysql.connector.Error as err:
        conn.rollback()
        result_text = f"Error during checkout: {err}"
    finally:
        cursor.close()
        conn.close()

    return result_text, sql_query_executed

# GUI Implementation
class LMSApp:
    def __init__(self, root):
        self.root = root
        root.title("Library Management System")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Create Tabs
        self.create_checkout_tab()
        # self.create_add_borrower_tab()
        # self.create_add_book_tab()
        # self.create_loaned_copies_tab()
        # self.create_late_returns_tab()
        # self.create_borrower_late_fees_tab()
        # self.create_borrower_book_late_fees_tab()

    def create_checkout_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Checkout Book")

        ttk.Label(tab, text="Checkout a book to a borrower.").pack(pady=5)

        frame = ttk.Frame(tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.checkout_book_id_entry = ttk.Entry(frame)
        self.checkout_book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Branch ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.checkout_branch_id_entry = ttk.Entry(frame)
        self.checkout_branch_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Borrower Card No:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.checkout_card_no_entry = ttk.Entry(frame)
        self.checkout_card_no_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(tab, text="Checkout Book", command=self.on_checkout_book).pack(pady=10)

        ttk.Label(tab, text="Result:").pack(pady=5)
        self.checkout_result_text = tk.Text(tab, height=5, width=60)
        self.checkout_result_text.pack(pady=5)

        ttk.Label(tab, text="SQL Query Executed:").pack(pady=5)
        self.checkout_sql_text = tk.Text(tab, height=5, width=60)
        self.checkout_sql_text.pack(pady=5)


    def on_checkout_book(self):
        book_id = self.checkout_book_id_entry.get()
        branch_id = self.checkout_branch_id_entry.get()
        card_no = self.checkout_card_no_entry.get()

        if not book_id or not branch_id or not card_no:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Basic input validation (check if they are digits)
        if not book_id.isdigit() or not branch_id.isdigit() or not card_no.isdigit():
             messagebox.showwarning("Input Error", "Book ID, Branch ID, and Card No must be numbers.")
             return

        result, sql_query = checkout_book(int(book_id), int(branch_id), int(card_no))
        self.checkout_result_text.delete(1.0, tk.END)
        self.checkout_result_text.insert(tk.END, result)
        self.checkout_sql_text.delete(1.0, tk.END)
        self.checkout_sql_text.insert(tk.END, sql_query)


# Main Application Execution
if __name__ == "__main__":
    # Basic check for database config
    if 'your_mysql_user' in DB_CONFIG.values():
        messagebox.showwarning("Configuration Needed", "Please update DB_CONFIG with your MySQL credentials before running.")
    else:
        root = tk.Tk()
        app = LMSApp(root)
        root.mainloop()