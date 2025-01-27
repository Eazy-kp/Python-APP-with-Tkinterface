import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re

def jls_extract_def():
    return None  # Dummy placeholder to prevent errors

class Donation:
    def __init__(self, root):  # Corrected constructor method name
        self.root = root
        self.root.title("Charity Donation Management System")
        self.root.geometry("500x500")
        self.db_connection = sqlite3.connect("charity_db.sqlite")
        self.db_cursor = self.db_connection.cursor()
        self.setup_database()
        self.create_main_ui()

    def setup_database(self):
        # Create tables for users, donations, and projects
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                role TEXT
            )
        """)
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT
            )
        """)
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                project_id INTEGER,
                amount REAL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)
        # Add a default admin user if it doesn't already exist
        self.db_cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if self.db_cursor.fetchone()[0] == 0:
            self.db_cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                                   ("admin", "admin123", "admin@gmail.com", "admin"))
        self.db_connection.commit()

    def create_main_ui(self):
        self.root.config(bg="#ADD8E6")
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#ADD8E6")
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="Welcome to Our Charity Donating System", font=("Helvetica", 16), bg="#ADD8E6").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(main_frame, text="Sign In", command=self.create_sign_in_ui, bg="#ADD8E6").grid(row=1, column=0, pady=10, padx=10)
        tk.Button(main_frame, text="Sign Up", command=self.create_sign_up_ui, bg="#ADD8E6").grid(row=1, column=1, pady=10)

        # Footer Section
        footer = tk.Label(self.root, text="Charity Donation Management System © 2025", bg="#ADD8E6", fg="black")
        footer.pack(side="bottom", fill="x", pady=5)

    def create_sign_in_ui(self):
        sign_in_window = tk.Toplevel(self.root)
        sign_in_window.title("Sign In")
        sign_in_window.geometry("350x300")
        sign_in_window.config(bg="#ADD8E6")

        tk.Label(sign_in_window, text="Username:", bg="#ADD8E6").grid(row=0, column=0, pady=5)
        username_entry = tk.Entry(sign_in_window)
        username_entry.grid(row=0, column=1, pady=5)

        tk.Label(sign_in_window, text="Password:", bg="#ADD8E6").grid(row=1, column=0, pady=5)
        password_entry = tk.Entry(sign_in_window, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        def handle_login():
            username = username_entry.get()
            password = password_entry.get()
            self.db_cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = self.db_cursor.fetchone()
            if user:
                if user[4] == "admin":
                    self.show_admin_ui()
                else:
                    self.show_donation_ui(user[0], username)
                sign_in_window.destroy() 
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        tk.Button(sign_in_window, text="Sign In", command=handle_login, bg="#ADD8E6").grid(row=2, columnspan=2, pady=10)

    def create_sign_up_ui(self):
        sign_up_window = tk.Toplevel(self.root)
        sign_up_window.title("Sign Up")
        sign_up_window.geometry("350x350")
        sign_up_window.config(bg="#ADD8E6")

        tk.Label(sign_up_window, text="Username:", bg="#ADD8E6").grid(row=0, column=0, pady=5)
        username_entry = tk.Entry(sign_up_window)
        username_entry.grid(row=0, column=1, pady=5)

        tk.Label(sign_up_window, text="Password:", bg="#ADD8E6").grid(row=1, column=0, pady=5)
        password_entry = tk.Entry(sign_up_window, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        tk.Label(sign_up_window, text="Confirm Password:", bg="#ADD8E6").grid(row=2, column=0, pady=5)
        confirm_password_entry = tk.Entry(sign_up_window, show="*")
        confirm_password_entry.grid(row=2, column=1, pady=5)

        tk.Label(sign_up_window, text="Email:", bg="#ADD8E6").grid(row=3, column=0, pady=5)
        email_entry = tk.Entry(sign_up_window)
        email_entry.grid(row=3, column=1, pady=5)

        def handle_sign_up():
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            email = email_entry.get()

            if not username or not password or not confirm_password or not email:
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            if not self.is_valid_email(email):
                messagebox.showerror("Error", "Invalid email address!")
                return

            try:
                self.db_cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                                       (username, password, email, "user"))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Sign Up Successful!")
                sign_up_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")

        tk.Button(sign_up_window, text="Sign Up", command=handle_sign_up, bg="#ADD8E6").grid(row=4, columnspan=2, pady=10)

    def show_admin_ui(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("500x400")
        admin_window.config(bg="#ADD8E6")

        tk.Button(admin_window, text="View Registered Users", command=self.view_users, bg="#ADD8E6").pack(pady=10)
        tk.Button(admin_window, text="View Donations", command=self.view_donations, bg="#ADD8E6").pack(pady=10)
        tk.Button(admin_window, text="Manage Projects", command=self.manage_projects, bg="#ADD8E6").pack(pady=10)

    def manage_projects(self):
        project_window = tk.Toplevel(self.root)
        project_window.title("Manage Projects")
        project_window.geometry("400x400")
        project_window.config(bg="#ADD8E6")

        tk.Label(project_window, text="Existing Projects:", bg="#ADD8E6", font=("Helvetica", 12)).pack(pady=10)

        self.db_cursor.execute("SELECT id, name FROM projects")
        projects = self.db_cursor.fetchall()

        project_listbox = tk.Listbox(project_window, width=40)
        for project in projects:
            project_listbox.insert(tk.END, f"{project[0]} - {project[1]}")
        project_listbox.pack(pady=10)

        def add_project():
            name = name_entry.get()
            description = description_entry.get()
            if not name or not description:
                messagebox.showerror("Error", "Please provide both name and description.")
                return
            self.db_cursor.execute("INSERT INTO projects (name, description) VALUES (?, ?)", (name, description))
            self.db_connection.commit()
            messagebox.showinfo("Success", f"Project '{name}' added successfully!")
            project_window.destroy()
            self.manage_projects()  # Refresh the window

        def delete_project():
            selected = project_listbox.get(tk.ACTIVE)
            if not selected:
                messagebox.showerror("Error", "Please select a project to delete.")
                return
            project_id = int(selected.split(" - ")[0])
            self.db_cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Project deleted successfully!")
            project_window.destroy()
            self.manage_projects()  # Refresh the window

        
        tk.Label(project_window, text="Add New Project:", bg="#ADD8E6", font=("Helvetica", 12)).pack(pady=10)
        tk.Label(project_window, text="Name:", bg="#ADD8E6").pack()
        name_entry = tk.Entry(project_window)
        name_entry.pack(pady=5)
        tk.Label(project_window, text="Description:", bg="#ADD8E6").pack()
        description_entry = tk.Entry(project_window)
        description_entry.pack(pady=5)
        tk.Button(project_window, text="Add Project", command=add_project, bg="#ADD8E6").pack(pady=10)
        tk.Button(project_window, text="Delete Selected Project", command=delete_project, bg="#ADD8E6").pack(pady=10)

        def go_back():
            project_window.destroy()
            self.show_admin_ui()

    def add_new_donor(self):
        add_donor_window = tk.Toplevel(self.root)
        add_donor_window.title("Add New Donor")
        add_donor_window.geometry("350x300")
        add_donor_window.config(bg="#ADD8E6")

        tk.Label(add_donor_window, text="Username:", bg="#ADD8E6").grid(row=0, column=0, pady=5, padx=10)
        username_entry = tk.Entry(add_donor_window)
        username_entry.grid(row=0, column=1, pady=5)

        tk.Label(add_donor_window, text="Password:", bg="#ADD8E6").grid(row=1, column=0, pady=5, padx=10)
        password_entry = tk.Entry(add_donor_window, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        tk.Label(add_donor_window, text="Email:", bg="#ADD8E6").grid(row=2, column=0, pady=5, padx=10)
        email_entry = tk.Entry(add_donor_window)
        email_entry.grid(row=2, column=1, pady=5)

        def handle_add_donor():
            username = username_entry.get()
            password = password_entry.get()
            email = email_entry.get()

            if not username or not password or not email:
                messagebox.showerror("Error", "All fields are required!")
                return

            if not self.is_valid_email(email):
                messagebox.showerror("Error", "Invalid email address!")
                return

            try:
                self.db_cursor.execute(
                    "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                    (username, password, email, "user"),
                )
                self.db_connection.commit()
                messagebox.showinfo("Success", "New donor added successfully!")
                add_donor_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")

        tk.Button(add_donor_window, text="Add Donor", command=handle_add_donor, bg="#ADD8E6").grid(row=3, columnspan=2, pady=10)
        
        def go_back():
            add_donor_window.destroy()  # Corrected from project_window to add_donor_window
            self.show_admin_ui()

    def view_users(self): 
        view_users_window = tk.Toplevel(self.root)
        view_users_window.title("Registered Users")
        view_users_window.geometry("500x400")
        view_users_window.config(bg="#ADD8E6")

        tk.Label(view_users_window, text="Registered Users:", bg="#ADD8E6", font=("Helvetica", 12)).pack(pady=10)

        self.db_cursor.execute("SELECT id, username, email, role FROM users")
        users = self.db_cursor.fetchall()

        users_listbox = tk.Listbox(view_users_window, width=50, height=15)
        for user in users:
            users_listbox.insert(tk.END, f"ID: {user[0]} | Username: {user[1]} | Email: {user[2]} | Role: {user[3]}")
        users_listbox.pack(pady=10)

        def go_back():
            view_users_window.destroy()
            self.show_admin_ui()

        tk.Button(view_users_window, text="Back to Admin Panel", command=go_back, bg="#ADD8E6").pack(pady=10)

    def view_donations(self):
        view_donations_window = tk.Toplevel(self.root)
        view_donations_window.title("All Donations")
        view_donations_window.geometry("600x400")
        view_donations_window.config(bg="#ADD8E6")

        tk.Label(view_donations_window, text="All Donations:", bg="#ADD8E6", font=("Helvetica", 12)).pack(pady=10)

        self.db_cursor.execute("""
            SELECT donations.id, users.username, projects.name, donations.amount
            FROM donations
            JOIN users ON donations.user_id = users.id
            JOIN projects ON donations.project_id = projects.id
        """)
        donations = self.db_cursor.fetchall()

        donations_listbox = tk.Listbox(view_donations_window, width=60, height=15)
        for donation in donations:
            donations_listbox.insert(tk.END, f"Donation ID: {donation[0]} | User: {donation[1]} | Project: {donation[2]} | Amount: {donation[3]}")
        donations_listbox.pack(pady=10)

        if not donations:
            tk.Label(view_donations_window, text="No donations have been made yet.", bg="#ADD8E6").pack()

        def go_back():
            view_donations_window.destroy()
            self.show_admin_ui()

        tk.Button(view_donations_window, text="Back to Admin Panel", command=go_back, bg="#ADD8E6").pack(pady=10)

    def show_donation_ui(self, user_id, username):
        donation_window = tk.Toplevel(self.root)
        donation_window.title("Make a Donation")
        donation_window.geometry("400x400")
        donation_window.config(bg="#ADD8E6")

        tk.Label(donation_window, text="Select Project to Donate to:", bg="#ADD8E6").pack(pady=10)

        self.db_cursor.execute("SELECT id, name FROM projects")
        projects = self.db_cursor.fetchall()

        project_combobox = ttk.Combobox(donation_window, values=[project[1] for project in projects], width=40)
        project_combobox.pack(pady=10)

        tk.Label(donation_window, text="Donation Amount:", bg="#ADD8E6").pack(pady=5)
        amount_entry = tk.Entry(donation_window)
        amount_entry.pack(pady=10)

        def make_donation():
            selected_project_name = project_combobox.get()
            amount = amount_entry.get()

            if not selected_project_name or not amount:
                messagebox.showerror("Error", "Please fill in both fields!")
                return

            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Invalid donation amount!")
                return

            self.db_cursor.execute("SELECT id FROM projects WHERE name = ?", (selected_project_name,))
            project_id = self.db_cursor.fetchone()[0]

            self.db_cursor.execute("INSERT INTO donations (user_id, project_id, amount) VALUES (?, ?, ?)",
                                   (user_id, project_id, amount))
            self.db_connection.commit()

            messagebox.showinfo("Success", "Donation successful! Thanks for your contribution.")
            donation_window.destroy()

        tk.Button(donation_window, text="Donate", command=make_donation, bg="#ADD8E6").pack(pady=10)

        def go_back():
            donation_window.destroy()
            self.create_main_ui()

        tk.Button(donation_window, text="Back", command=go_back, bg="#ADD8E6").pack(pady=10)

    def is_valid_email(self, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        return re.match(regex, email)

if __name__ == "__main__": 
    root = tk.Tk()
    app = Donation(root)
    root.mainloop()
