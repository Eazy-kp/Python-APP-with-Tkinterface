import tkinter as tk
from tkinter import messagebox
import random


class Donor:
    """A basic class for donor data."""
    def __init__(self, donor_id, name, email, username, password):
        self.donor_id = donor_id
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.donations = []

    def login(self, username, password):
        return username == self.username and password == self.password


class DonorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Charity Donation Management System")
        self.root.geometry("500x400")
        self.root.configure(bg="#E6E6FA")  # Light purple background

        # Mock database of donors
        self.donor_list = {
            "KIPONYA10": Donor(1, "Kiponya", "kiponya@gmail.com", "KIPONYA10", "password123")
        }

        # Available colors for dynamic elements
        self.colors = ["#FFEB3B", "#FF5722", "#4CAF50", "#2196F3", "#E91E63", "#9C27B0", "#3F51B5"]

        # Setup the login UI
        self.setup_login_ui()

        # Start the dynamic color change
        self.dynamic_color_change()

    def setup_login_ui(self):
        """Setup the Login Interface."""
        self.clear_frame()

        # Title Label
        self.title_label = tk.Label(
            self.root,
            text="Login",
            font=("Arial", 22, "bold"),
            bg="#9C27B0",  # Initial purple color for the title
            fg="white"
        )
        self.title_label.pack(pady=20)

        # Username Label and Entry
        tk.Label(
            self.root,
            text="Username:",
            font=("Arial", 12),
            bg="#E6E6FA"  # Light purple to match background
        ).pack(anchor="w", padx=40, pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.username_entry.pack(padx=40)

        # Password Label and Entry
        tk.Label(
            self.root,
            text="Password:",
            font=("Arial", 12),
            bg="#E6E6FA"
        ).pack(anchor="w", padx=40, pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show="*", width=25)
        self.password_entry.pack(padx=40)

        # Login Button
        self.login_button = tk.Button(
            self.root,
            text="Login",
            font=("Arial", 14, "bold"),
            bg="#FF5722",  # Initial orange color
            fg="white",
            activebackground="#E64A19",
            activeforeground="white",
            command=self.login,
            height=2,
            width=16
        )
        self.login_button.pack(pady=15)

        # Signup Button
        self.signup_button = tk.Button(
            self.root,
            text="Sign Up",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",  # Initial green color
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            command=self.setup_signup_ui,
            height=2,
            width=15
        )
        self.signup_button.pack(pady=5)

    def setup_signup_ui(self):
        """Setup the Signup Interface."""
        self.clear_frame()

        # Title Label
        self.title_label = tk.Label(
            self.root,
            text="Sign Up",
            font=("Arial", 22, "bold"),
            bg="#9C27B0",  # Initial purple color for the title
            fg="white"
        )
        self.title_label.pack(pady=20)

        # Input Fields
        self.signup_name = self.create_label_and_entry("Name:")
        self.signup_email = self.create_label_and_entry("Email:")
        self.signup_username = self.create_label_and_entry("Username:")
        self.signup_password = self.create_label_and_entry("Password:", show="*")

        # Signup Button
        self.signup_button = tk.Button(
            self.root,
            text="Register",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",  # Initial green color
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            command=self.register_user,
            height=3,
            width=16
        )
        self.signup_button.pack(pady=15)

        # Back to Login Button
        tk.Button(
            self.root,
            text="Back to Login",
            font=("Arial", 12),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            command=self.setup_login_ui
        ).pack(pady=5)

    def create_label_and_entry(self, label_text, show=None):
        """Helper to create a label and entry."""
        tk.Label(
            self.root,
            text=label_text,
            font=("Arial", 12),
            bg="#E6E6FA"
        ).pack(anchor="w", padx=40, pady=5)
        entry = tk.Entry(self.root, font=("Arial", 12), width=25, show=show)
        entry.pack(padx=40, pady=5)
        return entry

    def clear_frame(self):
        """Clear all widgets from the frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        """Handle the login process."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        donor = self.donor_list.get(username)
        if donor and donor.login(username, password):
            messagebox.showinfo("Success", f"Welcome, {donor.name}!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register_user(self):
        """Handle user registration."""
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()

        if not (name and email and username and password):
            messagebox.showerror("Error", "All fields are required!")
            return

        if username in self.donor_list:
            messagebox.showerror("Error", "Username already exists!")
            return

        # Add new donor to the donor list
        new_donor = Donor(len(self.donor_list) + 1, name, email, username, password)
        self.donor_list[username] = new_donor
        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        self.setup_login_ui()

    def dynamic_color_change(self):
        """Change the color of the title and buttons dynamically."""
        new_color = random.choice(self.colors)

        # Update background colors
        if hasattr(self, "title_label"):
            self.title_label.config(bg=new_color)

        if hasattr(self, "login_button"):
            self.login_button.config(bg=new_color)

        if hasattr(self, "signup_button"):
            self.signup_button.config(bg=new_color)

        # Schedule the next color change
        self.root.after(1000, self.dynamic_color_change)


if __name__ == "__main__":
    root = tk.Tk()
    app = DonorApp(root)
    root.mainloop()
