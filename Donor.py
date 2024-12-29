class Donor:
    def __init__(self, donor_id, name, email, username, password):
        self.__donor_id = donor_id
        self.__name = name
        self.__email = email
        self.__username = username
        self.__password = password
        self.__is_logged_in = False
        self.__donations = []  # Stores donation records

    def login(self, username, password):
        if self.__username == username and self.__password == password:
            self.__is_logged_in = True
            return True
        return False

    def logout(self):
        if self.__is_logged_in:
            self.__is_logged_in = False
            return True
        return False

    def make_donation(self, donation_amount):
        if self.__is_logged_in:
            self.__donations.append(donation_amount)
            return f"Donation of ${donation_amount} made successfully."
        return "You must log in first to make a donation."

    def view_donations(self):
        if not self.__donations:
            return "No donations made yet."
        summary = "\n".join([f" - ${amount}" for amount in self.__donations])
        return f"Donations:\n{summary}"





