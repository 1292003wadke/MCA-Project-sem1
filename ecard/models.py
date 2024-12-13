from django.db import models
from cryptography.fernet import Fernet
from django.contrib.auth.models import User

# Encryption utility
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher_suite = Fernet(key)

class ECard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_data = models.TextField(null=True, blank=True)  # Allow null and blank
    issued_at = models.DateTimeField(auto_now_add=True)
    ecard_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"E-Card for {self.user.username}"

    def generate_card(self):
        # Example logic for generating a virtual e-card
        return f"Virtual E-Card for {self.user.username} issued on {self.issued_at}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhaar = models.CharField(max_length=12, blank=True, null=True)
    pan = models.CharField(max_length=10, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    bank_details = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("In Process", "In Process"), ("Rejected", "Rejected"), ("Approved", "Approved")],
        default="In Process",
    )
    ecard_generated = models.BooleanField(default=False)  # Add this field
    def __str__(self):
        return self.user.username

    def encrypt_data(self):
        if self.aadhaar:
            self.aadhaar = cipher_suite.encrypt(self.aadhaar.encode()).decode()
        if self.pan:
            self.pan = cipher_suite.encrypt(self.pan.encode()).decode()
        if self.mobile_number:
            self.mobile_number = cipher_suite.encrypt(self.mobile_number.encode()).decode()
        if self.bank_details:
            self.bank_details = cipher_suite.encrypt(self.bank_details.encode()).decode()

    def decrypt_data(self):
        if self.aadhaar:
            self.aadhaar = cipher_suite.decrypt(self.aadhaar.encode()).decode()
        if self.pan:
            self.pan = cipher_suite.decrypt(self.pan.encode()).decode()
        if self.mobile_number:
            self.mobile_number = cipher_suite.decrypt(self.mobile_number.encode()).decode()
        if self.bank_details:
            self.bank_details = cipher_suite.decrypt(self.bank_details.encode()).decode()

    def generate_virtual_e_card(self):
        self.decrypt_data()
        return (
            f"Virtual E-Card for Aadhaar: {self.aadhaar}\nPAN: {self.pan}\n"
            f"Mobile: {self.mobile_number}\nBank Details: {self.bank_details}"
        )
