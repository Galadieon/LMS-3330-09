import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import datetime
from datetime import timedelta

# MySQL database credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1"
DB_NAME = "LMS"

class LMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LMS Application")
        self.root.geometry("1500x1000")

        self.db_connection = None
        self.connect_db()

        if not self.db_connection:
            messagebox.showerror("Database Connection Error", "Could not connect to the database.")
            self.root.destroy()
            return

        self.create_widgets()

    def connect_db(self):
        """Establishes a connection to the MySQL database."""
        try:
            self.db_connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.db_connection.is_connected():
                print("Database connection successful")
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.db_connection = None

    def close_db(self):
        """Closes the database connection."""
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            print("Database connection closed")

    def create_widgets(self):
        """Creates the main GUI widgets."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Create tabs for each task/query group
        self.tab_task2_q1 = ttk.Frame(self.notebook)
        self.tab_task2_q2 = ttk.Frame(self.notebook)
        self.tab_task2_q3 = ttk.Frame(self.notebook)
        self.tab_task2_q4 = ttk.Frame(self.notebook)
        self.tab_task2_q5 = ttk.Frame(self.notebook) # New tab for Q5
        self.tab_task2_q6a = ttk.Frame(self.notebook)
        self.tab_task2_q6b = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_task2_q1, text='Q1 (Checkout)')
        self.notebook.add(self.tab_task2_q2, text='Q2 (Add Borrower)')
        self.notebook.add(self.tab_task2_q3, text='Q3 (Add Book)')
        self.notebook.add(self.tab_task2_q4, text='Q4 (Copies Loaned)')
        self.notebook.add(self.tab_task2_q5, text='Q5 (Late Loans by Due Date)') # Add Q5 tab
        self.notebook.add(self.tab_task2_q6a, text='Q6a (Borrower Late Fees)')
        self.notebook.add(self.tab_task2_q6b, text='Q6b (Book Loan Info)')

        # Populate tabs with specific query interfaces
        self.setup_tab_task2_q1()
        self.setup_tab_task2_q2()
        self.setup_tab_task2_q3()
        self.setup_tab_task2_q4()
        self.setup_tab_task2_q5() # Setup the late loans tab
        # Add methods to setup other tabs similarly

    def setup_tab_task2_q1(self):
        """Sets up the interface for Query 1 (Checkout Book)."""
        frame = self.tab_task2_q1

        ttk.Label(frame, text="Checkout Book", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: Allow a borrower to check out a book.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q1_book_title_entry = ttk.Entry(input_frame, width=40)
        self.q1_book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Borrower Card Number:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q1_card_number_entry = ttk.Entry(input_frame, width=40)
        self.q1_card_number_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Date Out (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.q1_date_out_entry = ttk.Entry(input_frame, width=40)
        self.q1_date_out_entry.grid(row=2, column=1, padx=5, pady=5)
        self.q1_date_out_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d')) # Pre-fill with today's date

        # Updated label to indicate due date is calculated
        ttk.Label(input_frame, text="Due Date (Calculated - 31 days from Date Out):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.q1_due_date_display = ttk.Label(input_frame, text="") # Use a Label to display calculated date
        self.q1_due_date_display.grid(row=3, column=1, padx=5, pady=5, sticky="w")


        ttk.Button(frame, text="Checkout Book", command=self.execute_task2_q1).pack(pady=10)

        self.q1_output_label = ttk.Label(frame, text="")
        self.q1_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Queries Executed:").pack(pady=5)
        self.q1_sql_query_text = tk.Text(frame, height=6, width=70, state='disabled')
        self.q1_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Book Copies Output:").pack(pady=5)
        # Using Treeview for better tabular display of Book_Copies
        self.q1_copies_output_tree = ttk.Treeview(frame, columns=('book_id', 'branch_id', 'no_of_copies'), show='headings')
        self.q1_copies_output_tree.heading('book_id', text='Book ID')
        self.q1_copies_output_tree.heading('branch_id', text='Branch ID')
        self.q1_copies_output_tree.heading('no_of_copies', text='No. of Copies')
        self.q1_copies_output_tree.column('book_id', width=100, anchor='center')
        self.q1_copies_output_tree.column('branch_id', width=100, anchor='center')
        self.q1_copies_output_tree.column('no_of_copies', width=100, anchor='center')
        self.q1_copies_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q1(self):
        """Executes the queries for Query 1 (Checkout Book)."""
        book_title = self.q1_book_title_entry.get()
        card_number = self.q1_card_number_entry.get()
        date_out_str = self.q1_date_out_entry.get()
        returned_date = None # Returned_date is NULL on checkout
        late = 0 # Late is 0 on checkout

        if not book_title or not card_number or not date_out_str:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        try:
            # Parse date_out string to a date object
            date_out = datetime.datetime.strptime(date_out_str, '%Y-%m-%d').date()
            # Calculate due date (31 days after date_out)
            due_date = date_out + timedelta(days=31)
            due_date_str = due_date.strftime('%Y-%m-%d') # Format back to string

            # Update the displayed due date
            self.q1_due_date_display.config(text=due_date_str)

        except ValueError:
            messagebox.showwarning("Date Format Error", "Please enter Date Out in YYYY-MM-DD format.")
            return


        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # 1. Retrieve book_id of selected book title
            sql_select_book_id = "SELECT book_id FROM Book WHERE title = %s"
            cursor.execute(sql_select_book_id, (book_title,))
            book_output = cursor.fetchone()

            if not book_output:
                messagebox.showwarning("Book Not Found", f"Book with title '{book_title}' not found.")
                return
            selected_book_id = book_output[0]

            # 2. Retrieve branch_id where the book is available
            sql_select_branch_id = "SELECT branch_id FROM Book_Copies WHERE book_id = %s AND no_of_copies > 0 LIMIT 1"
            cursor.execute(sql_select_branch_id, (selected_book_id,))
            branch_output = cursor.fetchone()

            if not branch_output:
                messagebox.showwarning("Book Not Available", f"No copies of '{book_title}' available at any branch.")
                return
            branch_id = branch_output[0]

            # Display the queries being executed
            self.q1_sql_query_text.config(state='normal')
            self.q1_sql_query_text.delete(1.0, tk.END)
            self.q1_sql_query_text.insert(tk.END, f"SELECT book_id FROM Book WHERE title = '{book_title}';\n")
            self.q1_sql_query_text.insert(tk.END, f"SELECT branch_id FROM Book_Copies WHERE book_id = {selected_book_id} AND no_of_copies > 0 LIMIT 1;\n")


            # 3. Add new book checkout to Book_Loans
            sql_insert_loan = "INSERT INTO Book_Loans (book_id, branch_id, card_no, date_out, due_date, Returned_date, Late) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            loan_values = (selected_book_id, branch_id, card_number, date_out_str, due_date_str, returned_date, late)
            cursor.execute(sql_insert_loan, loan_values)
            self.db_connection.commit()

            self.q1_sql_query_text.insert(tk.END, f"INSERT INTO Book_Loans (book_id, branch_id, card_no, date_out, due_date, Returned_date, Late) VALUES ({selected_book_id}, {branch_id}, {card_number}, '{date_out_str}', '{due_date_str}', NULL, 0);\n")

            # 4. Update number of copies in Book_Copies (decrement)
            sql_update_copies = "UPDATE Book_Copies SET no_of_copies = no_of_copies - 1 WHERE book_id = %s AND branch_id = %s"
            update_values = (selected_book_id, branch_id)
            cursor.execute(sql_update_copies, update_values)
            self.db_connection.commit()

            self.q1_sql_query_text.insert(tk.END, f"UPDATE Book_Copies SET no_of_copies = no_of_copies - 1 WHERE book_id = {selected_book_id} AND branch_id = {branch_id};\n")
            self.q1_sql_query_text.config(state='disabled')


            # 5. Show the output of the updated Book_Copies
            sql_select_updated_copies = "SELECT book_id, branch_id, no_of_copies FROM Book_Copies WHERE book_id = %s AND branch_id = %s"
            cursor.execute(sql_select_updated_copies, (selected_book_id, branch_id))
            updated_copies_result = cursor.fetchall()

            # Clear previous results in the Treeview
            for item in self.q1_copies_output_tree.get_children():
                self.q1_copies_output_tree.delete(item)

            # Insert updated copies data into the Treeview
            for row in updated_copies_result:
                self.q1_copies_output_tree.insert('', tk.END, values=row)

            output_message = f"Book '{book_title}' checked out successfully to borrower {card_number} from branch {branch_id}. Due Date: {due_date_str}"
            self.q1_output_label.config(text=output_message)

            print(f"Action output: Book loan recorded, Book_Copies updated for book_id {selected_book_id}, branch_id {branch_id}.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error during book checkout: {e}")
            print(f"Error during book checkout: {e}")
            if self.db_connection:
                 self.db_connection.rollback() # Roll back changes if something goes wrong
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()


    def setup_tab_task2_q2(self):
        """Sets up the interface for Query 2 (Add New Borrower)."""
        frame = self.tab_task2_q2

        ttk.Label(frame, text="Add New Borrower", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: Add information for a new library borrower.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q2_name_entry = ttk.Entry(input_frame, width=40)
        self.q2_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q2_address_entry = ttk.Entry(input_frame, width=40)
        self.q2_address_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.q2_phone_entry = ttk.Entry(input_frame, width=40)
        self.q2_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Borrower", command=self.execute_task2_q2).pack(pady=10)

        self.q2_output_label = ttk.Label(frame, text="")
        self.q2_output_label.pack(pady=10)

        self.q2_sql_query_label = ttk.Label(frame, text="SQL Query:")
        self.q2_sql_query_label.pack(pady=5)
        self.q2_sql_query_text = tk.Text(frame, height=3, width=70, state='disabled')
        self.q2_sql_query_text.pack(pady=5)

        self.q2_result_label = ttk.Label(frame, text="Result:")
        self.q2_result_label.pack(pady=5)
        self.q2_result_text = tk.Text(frame, height=5, width=70, state='disabled')
        self.q2_result_text.pack(pady=5)


    def execute_task2_q2(self):
        """Executes the query for Query 2 (Add New Borrower)."""
        name = self.q2_name_entry.get()
        address = self.q2_address_entry.get()
        phone = self.q2_phone_entry.get()

        if not name or not address or not phone:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()
            sql = "INSERT INTO Borrower(name, address, phone) VALUES (%s, %s, %s)"
            values = (name, address, phone)

            # Display the query being executed
            self.q2_sql_query_text.config(state='normal')
            self.q2_sql_query_text.delete(1.0, tk.END)
            self.q2_sql_query_text.insert(tk.END, f"INSERT INTO Borrower(name, address, phone) VALUES ('{name}', '{address}', '{phone}');")
            self.q2_sql_query_text.config(state='disabled')

            cursor.execute(sql, values)
            self.db_connection.commit()

            # Get the last inserted ID (the new Card_No)
            new_card_no = cursor.lastrowid

            output_message = f"New borrower '{name}' added successfully."
            self.q2_output_label.config(text=output_message)

            # Display the result (new card number)
            self.q2_result_text.config(state='normal')
            self.q2_result_text.delete(1.0, tk.END)
            self.q2_result_text.insert(tk.END, f"New Library Card Issued:\nCard Number: {new_card_no}")
            self.q2_result_text.config(state='disabled')

            print(f"Action output: New borrower added, Card_No: {new_card_no}")

        except Error as e:
            messagebox.showerror("Database Error", f"Error adding borrower: {e}")
            print(f"Error adding borrower: {e}")
            if self.db_connection:
                 self.db_connection.rollback() # Roll back changes if something goes wrong
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def setup_tab_task2_q3(self):
        """Sets up the interface for Query 3 (Add New Book)."""
        frame = self.tab_task2_q3

        ttk.Label(frame, text="Add New Book", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: Add a new book with publisher and author information to all branches.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q3_book_title_entry = ttk.Entry(input_frame, width=40)
        self.q3_book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Publisher Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q3_publisher_entry = ttk.Entry(input_frame, width=40)
        self.q3_publisher_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Author Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.q3_author_entry = ttk.Entry(input_frame, width=40)
        self.q3_author_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Book", command=self.execute_task2_q3).pack(pady=10)

        self.q3_output_label = ttk.Label(frame, text="")
        self.q3_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Queries Executed:").pack(pady=5)
        self.q3_sql_query_text = tk.Text(frame, height=8, width=70, state='disabled')
        self.q3_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Book Copies Added:").pack(pady=5)
        # Using Treeview to show the book copies added to each branch
        self.q3_copies_output_tree = ttk.Treeview(frame, columns=('branch_id', 'no_of_copies'), show='headings')
        self.q3_copies_output_tree.heading('branch_id', text='Branch ID')
        self.q3_copies_output_tree.heading('no_of_copies', text='No. of Copies Added')
        self.q3_copies_output_tree.column('branch_id', width=100, anchor='center')
        self.q3_copies_output_tree.column('no_of_copies', width=150, anchor='center')
        self.q3_copies_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q3(self):
        """Executes the queries for Query 3 (Add New Book)."""
        book_title = self.q3_book_title_entry.get()
        publisher_name = self.q3_publisher_entry.get()
        author_name = self.q3_author_entry.get()
        copies_per_branch = 5 # As per requirement

        if not book_title or not publisher_name or not author_name:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # Display the queries being executed
            self.q3_sql_query_text.config(state='normal')
            self.q3_sql_query_text.delete(1.0, tk.END)


            # 1. Add new book with publisher info
            sql_insert_book = "INSERT INTO Book(title, book_publisher) VALUES (%s, %s)"
            book_values = (book_title, publisher_name)
            cursor.execute(sql_insert_book, book_values)

            self.q3_sql_query_text.insert(tk.END, f"INSERT INTO Book(title, book_publisher) VALUES ('{book_title}', '{publisher_name}');\n")

            # 2. Retrieve book_id of newly added book
            selected_book_id = cursor.lastrowid

            # 3. Add author info of newly added book
            sql_insert_author = "INSERT INTO Book_Authors(book_id, author_name) VALUES (%s, %s)"
            author_values = (selected_book_id, author_name)
            cursor.execute(sql_insert_author, author_values)

            self.q3_sql_query_text.insert(tk.END, f"INSERT INTO Book_Authors(book_id, author_name) VALUES ({selected_book_id}, '{author_name}');\n")

            # 4. Retrieve number of library branches
            sql_count_branches = "SELECT COUNT(*) FROM Library_Branch"
            cursor.execute(sql_count_branches)
            count_of_library_branches = cursor.fetchone()[0]
            num_of_library_branches = int(count_of_library_branches)

            self.q3_sql_query_text.insert(tk.END, f"SELECT COUNT(*) FROM Library_Branch;\n")

            # Clear previous results in the Treeview
            for item in self.q3_copies_output_tree.get_children():
                self.q3_copies_output_tree.delete(item)

            # 5. Add 5 copies per branch for newly added book
            sql_insert_copies = "INSERT INTO Book_Copies(book_id, branch_id, no_of_copies) VALUES (%s, %s, %s)"
            for i in range(1, num_of_library_branches + 1):
                copies_values = (selected_book_id, i, copies_per_branch)
                cursor.execute(sql_insert_copies, copies_values)
                self.q3_sql_query_text.insert(tk.END, f"INSERT INTO Book_Copies(book_id, branch_id, no_of_copies) VALUES ({selected_book_id}, {i}, {copies_per_branch});\n")

                # Insert into Treeview to show copies added
                self.q3_copies_output_tree.insert('', tk.END, values=(i, copies_per_branch))

            # Commit all changes if all inserts were successful
            self.db_connection.commit()
            self.q3_sql_query_text.config(state='disabled')


            output_message = f"New book '{book_title}' by {author_name} (Publisher: {publisher_name}) added successfully with {copies_per_branch} copies at each of the {num_of_library_branches} branches."
            self.q3_output_label.config(text=output_message)

            print(f"Action output: New book added (book_id: {selected_book_id}), author added, and {copies_per_branch} copies added to {num_of_library_branches} branches.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error adding book: {e}")
            print(f"Error adding book: {e}")
            if self.db_connection:
                 self.db_connection.rollback() # Roll back changes if something goes wrong
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def setup_tab_task2_q4(self):
        """Sets up the interface for Query 4 (Copies Loaned per Branch)."""
        frame = self.tab_task2_q4

        ttk.Label(frame, text="Copies Loaned per Branch", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: List the number of copies loaned out per branch for a given book title.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q4_book_title_entry = ttk.Entry(input_frame, width=40)
        self.q4_book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="List Copies Loaned", command=self.execute_task2_q4).pack(pady=10)

        self.q4_output_label = ttk.Label(frame, text="")
        self.q4_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Query Executed:").pack(pady=5)
        self.q4_sql_query_text = tk.Text(frame, height=4, width=70, state='disabled')
        self.q4_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Copies Loaned Output:").pack(pady=5)
        # Using Treeview to display the copies loaned out per branch
        self.q4_copies_output_tree = ttk.Treeview(frame, columns=('book_id', 'book_title', 'branch_id', 'branch_name', 'num_of_copies_loaned'), show='headings')
        self.q4_copies_output_tree.heading('book_id', text='Book ID')
        self.q4_copies_output_tree.heading('book_title', text='Book Title')
        self.q4_copies_output_tree.heading('branch_id', text='Branch ID')
        self.q4_copies_output_tree.heading('branch_name', text='Branch Name')
        self.q4_copies_output_tree.heading('num_of_copies_loaned', text='Copies Loaned')
        self.q4_copies_output_tree.column('book_id', width=80, anchor='center')
        self.q4_copies_output_tree.column('book_title', width=200)
        self.q4_copies_output_tree.column('branch_id', width=80, anchor='center')
        self.q4_copies_output_tree.column('branch_name', width=150)
        self.q4_copies_output_tree.column('num_of_copies_loaned', width=120, anchor='center')
        self.q4_copies_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q4(self):
        """Executes the query for Query 4 (Copies Loaned per Branch)."""
        book_title = self.q4_book_title_entry.get()

        if not book_title:
            messagebox.showwarning("Input Error", "Please enter a book title.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # SQL query to list copies loaned out per branch for a given book title
            sql_query = """
                SELECT
                    Bk.book_id,
                    Bk.title,
                    B_L.branch_id,
                    L_B.branch_name,
                    COUNT(*) AS num_of_copies_loaned
                FROM Book AS Bk
                JOIN Book_Loans AS B_L ON Bk.book_id = B_L.book_id
                JOIN Library_Branch AS L_B ON B_L.branch_id = L_B.branch_id
                WHERE Bk.title = %s
                GROUP BY Bk.book_id, Bk.title, B_L.branch_id, L_B.branch_name;
            """
            values = (book_title,)

            # Display the query being executed
            self.q4_sql_query_text.config(state='normal')
            self.q4_sql_query_text.delete(1.0, tk.END)
            self.q4_sql_query_text.insert(tk.END, sql_query.replace('%s', f"'{book_title}'"))
            self.q4_sql_query_text.config(state='disabled')

            cursor.execute(sql_query, values)
            results = cursor.fetchall()

            # Clear previous results in the Treeview
            for item in self.q4_copies_output_tree.get_children():
                self.q4_copies_output_tree.delete(item)

            if not results:
                self.q4_output_label.config(text=f"No copies of '{book_title}' are currently loaned out.")
                print("Action output: 0 row(s) returned.")
            else:
                # Insert results into the Treeview
                for row in results:
                    self.q4_copies_output_tree.insert('', tk.END, values=row)
                self.q4_output_label.config(text=f"Copies loaned out for '{book_title}':")
                print(f"Action output: {len(results)} row(s) returned.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error listing copies loaned: {e}")
            print(f"Error listing copies loaned: {e}")
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def setup_tab_task2_q5(self):
        """Sets up the interface for Query 5 (Late Loans by Due Date Range)."""
        frame = self.tab_task2_q5

        ttk.Label(frame, text="Late Loans by Due Date Range", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: List book loans returned late within a specified due date range.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Start Due Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q5_start_date_entry = ttk.Entry(input_frame, width=40)
        self.q5_start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="End Due Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q5_end_date_entry = ttk.Entry(input_frame, width=40)
        self.q5_end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="List Late Loans", command=self.execute_task2_q5).pack(pady=10)

        self.q5_output_label = ttk.Label(frame, text="")
        self.q5_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Query Executed:").pack(pady=5)
        self.q5_sql_query_text = tk.Text(frame, height=8, width=70, state='disabled')
        self.q5_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Late Loans Output:").pack(pady=5)
        # Using Treeview to display the late loans information
        self.q5_late_loans_output_tree = ttk.Treeview(frame, columns=('book_id', 'branch_id', 'card_no', 'date_out', 'due_date', 'returned_date', 'num_of_days_late'), show='headings')
        self.q5_late_loans_output_tree.heading('book_id', text='Book ID')
        self.q5_late_loans_output_tree.heading('branch_id', text='Branch ID')
        self.q5_late_loans_output_tree.heading('card_no', text='Card No')
        self.q5_late_loans_output_tree.heading('date_out', text='Date Out')
        self.q5_late_loans_output_tree.heading('due_date', text='Due Date')
        self.q5_late_loans_output_tree.heading('returned_date', text='Returned Date')
        self.q5_late_loans_output_tree.heading('num_of_days_late', text='Days Late')
        self.q5_late_loans_output_tree.column('book_id', width=80, anchor='center')
        self.q5_late_loans_output_tree.column('branch_id', width=80, anchor='center')
        self.q5_late_loans_output_tree.column('card_no', width=100, anchor='center')
        self.q5_late_loans_output_tree.column('date_out', width=120, anchor='center')
        self.q5_late_loans_output_tree.column('due_date', width=120, anchor='center')
        self.q5_late_loans_output_tree.column('returned_date', width=120, anchor='center')
        self.q5_late_loans_output_tree.column('num_of_days_late', width=100, anchor='center')
        self.q5_late_loans_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q5(self):
        """Executes the query for Query 5 (Late Loans by Due Date Range)."""
        start_date_str = self.q5_start_date_entry.get()
        end_date_str = self.q5_end_date_entry.get()

        if not start_date_str or not end_date_str:
            messagebox.showwarning("Input Error", "Please enter both start and end due dates.")
            return

        try:
            # Validate date format
            datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Date Format Error", "Please enter dates in YYYY-MM-DD format.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # SQL query to list late book loans within a due date range
            sql_query = """
                SELECT
                    B_L.book_id,
                    B_L.branch_id,
                    B_L.card_no,
                    B_L.date_out,
                    B_L.due_date,
                    B_L.Returned_date,
                    CASE
                        WHEN B_L.Returned_date IS NULL OR DATEDIFF(B_L.Returned_date, B_L.due_date) <= 0 THEN 0
                        ELSE DATEDIFF(B_L.Returned_date, B_L.due_date)
                    END AS num_of_days_late
                FROM Book_Loans AS B_L
                WHERE B_L.due_date BETWEEN %s AND %s
                HAVING num_of_days_late > 0;
            """
            values = (start_date_str, end_date_str)

            # Display the query being executed
            self.q5_sql_query_text.config(state='normal')
            self.q5_sql_query_text.delete(1.0, tk.END)
            self.q5_sql_query_text.insert(tk.END, sql_query.replace('%s', "'{}'").format(start_date_str, end_date_str))
            self.q5_sql_query_text.config(state='disabled')


            cursor.execute(sql_query, values)
            results = cursor.fetchall()

            # Clear previous results in the Treeview
            for item in self.q5_late_loans_output_tree.get_children():
                self.q5_late_loans_output_tree.delete(item)

            if not results:
                self.q5_output_label.config(text=f"No late loans found with due dates between {start_date_str} and {end_date_str}.")
                print("Action output: 0 row(s) returned.")
            else:
                # Insert results into the Treeview
                for row in results:
                    # Format date objects to strings for display in Treeview
                    formatted_row = tuple(str(item) if isinstance(item, datetime.date) else item for item in row)
                    self.q5_late_loans_output_tree.insert('', tk.END, values=formatted_row)
                self.q5_output_label.config(text=f"Late loans with due dates between {start_date_str} and {end_date_str}:")
                print(f"Action output: {len(results)} row(s) returned.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error listing late loans: {e}")
            print(f"Error listing late loans: {e}")
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()


    def setup_tab_task2_q2(self):
        """Sets up the interface for Query 2 (Add New Borrower)."""
        frame = self.tab_task2_q2

        ttk.Label(frame, text="Add New Borrower", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: Add information for a new library borrower.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q2_name_entry = ttk.Entry(input_frame, width=40)
        self.q2_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q2_address_entry = ttk.Entry(input_frame, width=40)
        self.q2_address_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.q2_phone_entry = ttk.Entry(input_frame, width=40)
        self.q2_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Borrower", command=self.execute_task2_q2).pack(pady=10)

        self.q2_output_label = ttk.Label(frame, text="")
        self.q2_output_label.pack(pady=10)

        self.q2_sql_query_label = ttk.Label(frame, text="SQL Query:")
        self.q2_sql_query_label.pack(pady=5)
        self.q2_sql_query_text = tk.Text(frame, height=3, width=70, state='disabled')
        self.q2_sql_query_text.pack(pady=5)

        self.q2_result_label = ttk.Label(frame, text="Result:")
        self.q2_result_label.pack(pady=5)
        self.q2_result_text = tk.Text(frame, height=5, width=70, state='disabled')
        self.q2_result_text.pack(pady=5)


    def execute_task2_q2(self):
        """Executes the query for Query 2 (Add New Borrower)."""
        name = self.q2_name_entry.get()
        address = self.q2_address_entry.get()
        phone = self.q2_phone_entry.get()

        if not name or not address or not phone:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()
            sql = "INSERT INTO Borrower(name, address, phone) VALUES (%s, %s, %s)"
            values = (name, address, phone)

            # Display the query being executed
            self.q2_sql_query_text.config(state='normal')
            self.q2_sql_query_text.delete(1.0, tk.END)
            self.q2_sql_query_text.insert(tk.END, f"INSERT INTO Borrower(name, address, phone) VALUES ('{name}', '{address}', '{phone}');")
            self.q2_sql_query_text.config(state='disabled')

            cursor.execute(sql, values)
            self.db_connection.commit()

            # Get the last inserted ID (the new Card_No)
            new_card_no = cursor.lastrowid

            output_message = f"New borrower '{name}' added successfully."
            self.q2_output_label.config(text=output_message)

            # Display the result (new card number)
            self.q2_result_text.config(state='normal')
            self.q2_result_text.delete(1.0, tk.END)
            self.q2_result_text.insert(tk.END, f"New Library Card Issued:\nCard Number: {new_card_no}")
            self.q2_result_text.config(state='disabled')

            print(f"Action output: New borrower added, Card_No: {new_card_no}")

        except Error as e:
            messagebox.showerror("Database Error", f"Error adding borrower: {e}")
            print(f"Error adding borrower: {e}")
            if self.db_connection:
                 self.db_connection.rollback() # Roll back changes if something goes wrong
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def setup_tab_task2_q3(self):
        """Sets up the interface for Query 3 (Add New Book)."""
        frame = self.tab_task2_q3

        ttk.Label(frame, text="Add New Book", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: Add a new book with publisher and author information to all branches.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q3_book_title_entry = ttk.Entry(input_frame, width=40)
        self.q3_book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Publisher Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q3_publisher_entry = ttk.Entry(input_frame, width=40)
        self.q3_publisher_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Author Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.q3_author_entry = ttk.Entry(input_frame, width=40)
        self.q3_author_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Book", command=self.execute_task2_q3).pack(pady=10)

        self.q3_output_label = ttk.Label(frame, text="")
        self.q3_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Queries Executed:").pack(pady=5)
        self.q3_sql_query_text = tk.Text(frame, height=8, width=70, state='disabled')
        self.q3_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Book Copies Added:").pack(pady=5)
        # Using Treeview to show the book copies added to each branch
        self.q3_copies_output_tree = ttk.Treeview(frame, columns=('branch_id', 'no_of_copies'), show='headings')
        self.q3_copies_output_tree.heading('branch_id', text='Branch ID')
        self.q3_copies_output_tree.heading('no_of_copies', text='No. of Copies Added')
        self.q3_copies_output_tree.column('branch_id', width=100, anchor='center')
        self.q3_copies_output_tree.column('no_of_copies', width=150, anchor='center')
        self.q3_copies_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q3(self):
        """Executes the queries for Query 3 (Add New Book)."""
        book_title = self.q3_book_title_entry.get()
        publisher_name = self.q3_publisher_entry.get()
        author_name = self.q3_author_entry.get()
        copies_per_branch = 5 # As per requirement

        if not book_title or not publisher_name or not author_name:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # Display the queries being executed
            self.q3_sql_query_text.config(state='normal')
            self.q3_sql_query_text.delete(1.0, tk.END)


            # 1. Add new book with publisher info
            sql_insert_book = "INSERT INTO Book(title, book_publisher) VALUES (%s, %s)"
            book_values = (book_title, publisher_name)
            cursor.execute(sql_insert_book, book_values)

            self.q3_sql_query_text.insert(tk.END, f"INSERT INTO Book(title, book_publisher) VALUES ('{book_title}', '{publisher_name}');\n")

            # 2. Retrieve book_id of newly added book
            selected_book_id = cursor.lastrowid

            # 3. Add author info of newly added book
            sql_insert_author = "INSERT INTO Book_Authors(book_id, author_name) VALUES (%s, %s)"
            author_values = (selected_book_id, author_name)
            cursor.execute(sql_insert_author, author_values)

            self.q3_sql_query_text.insert(tk.END, f"INSERT INTO Book_Authors(book_id, author_name) VALUES ({selected_book_id}, '{author_name}');\n")

            # 4. Retrieve number of library branches
            sql_count_branches = "SELECT COUNT(*) FROM Library_Branch"
            cursor.execute(sql_count_branches)
            count_of_library_branches = cursor.fetchone()[0]
            num_of_library_branches = int(count_of_library_branches)

            self.q3_sql_query_text.insert(tk.END, f"SELECT COUNT(*) FROM Library_Branch;\n")

            # Clear previous results in the Treeview
            for item in self.q3_copies_output_tree.get_children():
                self.q3_copies_output_tree.delete(item)

            # 5. Add 5 copies per branch for newly added book
            sql_insert_copies = "INSERT INTO Book_Copies(book_id, branch_id, no_of_copies) VALUES (%s, %s, %s)"
            for i in range(1, num_of_library_branches + 1):
                copies_values = (selected_book_id, i, copies_per_branch)
                cursor.execute(sql_insert_copies, copies_values)
                self.q3_sql_query_text.insert(tk.END, f"INSERT INTO Book_Copies(book_id, branch_id, no_of_copies) VALUES ({selected_book_id}, {i}, {copies_per_branch});\n")

                # Insert into Treeview to show copies added
                self.q3_copies_output_tree.insert('', tk.END, values=(i, copies_per_branch))

            # Commit all changes if all inserts were successful
            self.db_connection.commit()
            self.q3_sql_query_text.config(state='disabled')


            output_message = f"New book '{book_title}' by {author_name} (Publisher: {publisher_name}) added successfully with {copies_per_branch} copies at each of the {num_of_library_branches} branches."
            self.q3_output_label.config(text=output_message)

            print(f"Action output: New book added (book_id: {selected_book_id}), author added, and {copies_per_branch} copies added to {num_of_library_branches} branches.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error adding book: {e}")
            print(f"Error adding book: {e}")
            if self.db_connection:
                 self.db_connection.rollback() # Roll back changes if something goes wrong
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def setup_tab_task2_q4(self):
        """Sets up the interface for Query 4 (Copies Loaned per Branch)."""
        frame = self.tab_task2_q4

        ttk.Label(frame, text="Copies Loaned per Branch", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: List the number of copies loaned out per branch for a given book title.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q4_book_title_entry = ttk.Entry(input_frame, width=40)
        self.q4_book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="List Copies Loaned", command=self.execute_task2_q4).pack(pady=10)

        self.q4_output_label = ttk.Label(frame, text="")
        self.q4_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Query Executed:").pack(pady=5)
        self.q4_sql_query_text = tk.Text(frame, height=4, width=70, state='disabled')
        self.q4_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Copies Loaned Output:").pack(pady=5)
        # Using Treeview to display the copies loaned out per branch
        self.q4_copies_output_tree = ttk.Treeview(frame, columns=('book_id', 'book_title', 'branch_id', 'branch_name', 'num_of_copies_loaned'), show='headings')
        self.q4_copies_output_tree.heading('book_id', text='Book ID')
        self.q4_copies_output_tree.heading('book_title', text='Book Title')
        self.q4_copies_output_tree.heading('branch_id', text='Branch ID')
        self.q4_copies_output_tree.heading('branch_name', text='Branch Name')
        self.q4_copies_output_tree.heading('num_of_copies_loaned', text='Copies Loaned')
        self.q4_copies_output_tree.column('book_id', width=80, anchor='center')
        self.q4_copies_output_tree.column('book_title', width=200)
        self.q4_copies_output_tree.column('branch_id', width=80, anchor='center')
        self.q4_copies_output_tree.column('branch_name', width=150)
        self.q4_copies_output_tree.column('num_of_copies_loaned', width=120, anchor='center')
        self.q4_copies_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q4(self):
        """Executes the query for Query 4 (Copies Loaned per Branch)."""
        book_title = self.q4_book_title_entry.get()

        if not book_title:
            messagebox.showwarning("Input Error", "Please enter a book title.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # SQL query to list copies loaned out per branch for a given book title
            sql_query = """
                SELECT
                    Bk.book_id,
                    Bk.title,
                    B_L.branch_id,
                    L_B.branch_name,
                    COUNT(*) AS num_of_copies_loaned
                FROM Book AS Bk
                JOIN Book_Loans AS B_L ON Bk.book_id = B_L.book_id
                JOIN Library_Branch AS L_B ON B_L.branch_id = L_B.branch_id
                WHERE Bk.title = %s
                GROUP BY Bk.book_id, Bk.title, B_L.branch_id, L_B.branch_name;
            """
            values = (book_title,)

            # Display the query being executed
            self.q4_sql_query_text.config(state='normal')
            self.q4_sql_query_text.delete(1.0, tk.END)
            self.q4_sql_query_text.insert(tk.END, sql_query.replace('%s', f"'{book_title}'"))
            self.q4_sql_query_text.config(state='disabled')

            cursor.execute(sql_query, values)
            results = cursor.fetchall()

            # Clear previous results in the Treeview
            for item in self.q4_copies_output_tree.get_children():
                self.q4_copies_output_tree.delete(item)

            if not results:
                self.q4_output_label.config(text=f"No copies of '{book_title}' are currently loaned out.")
                print("Action output: 0 row(s) returned.")
            else:
                # Insert results into the Treeview
                for row in results:
                    self.q4_copies_output_tree.insert('', tk.END, values=row)
                self.q4_output_label.config(text=f"Copies loaned out for '{book_title}':")
                print(f"Action output: {len(results)} row(s) returned.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error listing copies loaned: {e}")
            print(f"Error listing copies loaned: {e}")
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def setup_tab_task2_q5(self):
        """Sets up the interface for Query 5 (Late Loans by Due Date Range)."""
        frame = self.tab_task2_q5

        ttk.Label(frame, text="Late Loans by Due Date Range", font=('Arial', 14)).pack(pady=10)
        ttk.Label(frame, text="Query Purpose: List book loans returned late within a specified due date range.").pack(pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Start Due Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.q5_start_date_entry = ttk.Entry(input_frame, width=40)
        self.q5_start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="End Due Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.q5_end_date_entry = ttk.Entry(input_frame, width=40)
        self.q5_end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="List Late Loans", command=self.execute_task2_q5).pack(pady=10)

        self.q5_output_label = ttk.Label(frame, text="")
        self.q5_output_label.pack(pady=10)

        ttk.Label(frame, text="SQL Query Executed:").pack(pady=5)
        self.q5_sql_query_text = tk.Text(frame, height=8, width=70, state='disabled')
        self.q5_sql_query_text.pack(pady=5)

        ttk.Label(frame, text="Late Loans Output:").pack(pady=5)
        # Using Treeview to display the late loans information
        self.q5_late_loans_output_tree = ttk.Treeview(frame, columns=('book_id', 'branch_id', 'card_no', 'date_out', 'due_date', 'returned_date', 'num_of_days_late'), show='headings')
        self.q5_late_loans_output_tree.heading('book_id', text='Book ID')
        self.q5_late_loans_output_tree.heading('branch_id', text='Branch ID')
        self.q5_late_loans_output_tree.heading('card_no', text='Card No')
        self.q5_late_loans_output_tree.heading('date_out', text='Date Out')
        self.q5_late_loans_output_tree.heading('due_date', text='Due Date')
        self.q5_late_loans_output_tree.heading('returned_date', text='Returned Date')
        self.q5_late_loans_output_tree.heading('num_of_days_late', text='Days Late')
        self.q5_late_loans_output_tree.column('book_id', width=80, anchor='center')
        self.q5_late_loans_output_tree.column('branch_id', width=80, anchor='center')
        self.q5_late_loans_output_tree.column('card_no', width=100, anchor='center')
        self.q5_late_loans_output_tree.column('date_out', width=120, anchor='center')
        self.q5_late_loans_output_tree.column('due_date', width=120, anchor='center')
        self.q5_late_loans_output_tree.column('returned_date', width=120, anchor='center')
        self.q5_late_loans_output_tree.column('num_of_days_late', width=100, anchor='center')
        self.q5_late_loans_output_tree.pack(pady=5, fill="both", expand=True)


    def execute_task2_q5(self):
        """Executes the query for Query 5 (Late Loans by Due Date Range)."""
        start_date_str = self.q5_start_date_entry.get()
        end_date_str = self.q5_end_date_entry.get()

        if not start_date_str or not end_date_str:
            messagebox.showwarning("Input Error", "Please enter both start and end due dates.")
            return

        try:
            # Validate date format
            datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Date Format Error", "Please enter dates in YYYY-MM-DD format.")
            return

        cursor = None
        try:
            cursor = self.db_connection.cursor()

            # SQL query to list late book loans within a due date range
            sql_query = """
                SELECT
                    B_L.book_id,
                    B_L.branch_id,
                    B_L.card_no,
                    B_L.date_out,
                    B_L.due_date,
                    B_L.Returned_date,
                    CASE
                        WHEN B_L.Returned_date IS NULL OR DATEDIFF(B_L.Returned_date, B_L.due_date) <= 0 THEN 0
                        ELSE DATEDIFF(B_L.Returned_date, B_L.due_date)
                    END AS num_of_days_late
                FROM Book_Loans AS B_L
                WHERE B_L.due_date BETWEEN %s AND %s
                HAVING num_of_days_late > 0;
            """
            values = (start_date_str, end_date_str)

            # Display the query being executed
            self.q5_sql_query_text.config(state='normal')
            self.q5_sql_query_text.delete(1.0, tk.END)
            self.q5_sql_query_text.insert(tk.END, sql_query.replace('%s', "'{}'").format(start_date_str, end_date_str))
            self.q5_sql_query_text.config(state='disabled')


            cursor.execute(sql_query, values)
            results = cursor.fetchall()

            # Clear previous results in the Treeview
            for item in self.q5_late_loans_output_tree.get_children():
                self.q5_late_loans_output_tree.delete(item)

            if not results:
                self.q5_output_label.config(text=f"No late loans found with due dates between {start_date_str} and {end_date_str}.")
                print("Action output: 0 row(s) returned.")
            else:
                # Insert results into the Treeview
                for row in results:
                    # Format date objects to strings for display in Treeview
                    formatted_row = tuple(str(item) if isinstance(item, datetime.date) else item for item in row)
                    self.q5_late_loans_output_tree.insert('', tk.END, values=formatted_row)
                self.q5_output_label.config(text=f"Late loans with due dates between {start_date_str} and {end_date_str}:")
                print(f"Action output: {len(results)} row(s) returned.")

        except Error as e:
            messagebox.showerror("Database Error", f"Error listing late loans: {e}")
            print(f"Error listing late loans: {e}")
        except Exception as e:
             messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
             print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    def display_results_in_text(self, text_widget, results, columns):
        """Helper function to display query results in a text widget."""
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)

        if not results:
            text_widget.insert(tk.END, "No records found.")
            print("Action output: 0 row(s) returned.")
            text_widget.config(state='disabled')
            return

        # Display headers
        text_widget.insert(tk.END, "\t".join(columns) + "\n")
        text_widget.insert(tk.END, "-" * (8 * len(columns)) + "\n") # Simple separator

        # Display rows
        for row in results:
            text_widget.insert(tk.END, "\t".join(map(str, row)) + "\n")

        print(f"Action output: {len(results)} row(s) returned.")
        text_widget.config(state='disabled')

    def on_closing(self):
        """Handles cleanup when the application window is closed."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close_db()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LMSApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
