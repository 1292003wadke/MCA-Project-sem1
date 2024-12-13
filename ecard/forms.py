from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

# Reference the user model dynamically to support custom User models
User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User  # Dynamically fetched User model
        fields = ['username', 'password', 'email']  # Adjust as per your User model

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Ensure the password is hashed
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["aadhaar", "pan", "mobile_number", "bank_details"]

    def clean_aadhaar(self):
        aadhaar = self.cleaned_data.get("aadhaar")
        if aadhaar and len(aadhaar) != 12:
            raise forms.ValidationError("Aadhaar number must be 12 digits.")
        return aadhaar

    def clean_pan(self):
        pan = self.cleaned_data.get("pan")
        if pan and len(pan) != 10:
            raise forms.ValidationError("PAN number must be 10 characters.")
        return pan

