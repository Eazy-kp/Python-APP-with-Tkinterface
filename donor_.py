import tkinter as tk
from tkinter import messagebox

class Donor:
    def __init__(self, donor_id, name, email, username, password):
        self.donor_id = donor_id
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.donations = []
       
       
      

    def login(self, username, password):
        return username == self.username and password == self.password
    
    def login(self, emmmail, passwordd passwd='', acct='')

    def logout(self):
        pass  # For now, just a placeholder method.

    def make_donation(self, amount):
        self.donations.append(amount)
        return f"Donation of {amount} received. Thank you for your generosity!"

    def view_donations(self):
        return "\n".join([f"Donation: {donation}" for donation in self.donations]) or "No donations yet."


class DonorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Charity Donation Management System")
        self.root.geometry("800x500")

        # Active donor (mock data)
        self.donor = Donor(1, "Kiponya", "kiponya@gmail.com", "KIPONYA10", "password123")

        # UI Elements
        self.setup_login_ui()

    def setup_login_ui(self):
        self.clear_frame()

        tk.Label(self.root, text="Login", font=("Arial", 26)).pack(pady=20)

        tk.Label(self.root, text="Username:").pack(pady=15)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=15)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def setup_donor_ui(self):
        self.clear_frame()

        tk.Label(self.root, text=f"Welcome {self.donor.name}!", font=("Arial", 26)).pack(pady=20)

        tk.Button(self.root, text="Make a Donation", command=self.make_donation_ui).pack(pady=15)
        tk.Button(self.root, text="View Donations", command=self.view_donations).pack(pady=15)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def make_donation_ui(self):
        self.clear_frame()

        tk.Label(self.root, text="Make a Donation", font=("Arial", 26)).pack(pady=20)

        tk.Label(self.root, text="Amount:").pack(pady=15)
        self.donation_entry = tk.Entry(self.root)
        self.donation_entry.pack(pady=15)

        tk.Button(self.root, text="Donate", command=self.make_donation).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.setup_donor_ui).pack(pady=15)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.donor.login(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            self.setup_donor_ui()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def logout(self):
        self.donor.logout()
        messagebox.showinfo("Success", "Logged out successfully.")
        self.setup_login_ui()

    def make_donation(self):
        try:
            amount = float(self.donation_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            result = self.donor.make_donation(amount)
            messagebox.showinfo("Success", result)
            self.setup_donor_ui()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_donations(self):
        donations = self.donor.view_donations()
        messagebox.showinfo("Donations", donations)


if __name__ == "__main__":
    root = tk.Tk()
    app = DonorApp(root)
    root.mainloop()




