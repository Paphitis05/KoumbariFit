from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser

user = get_user_model()

# User Login Form
class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")


# User Registration Form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = user
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        """
        Overrides the save method to store a hashed password instead of plain text.
        """
        user = super().save(commit=False)  # Creates a user object but doesn't save to the database yet
        user.set_password(self.cleaned_data["password"])  # Hashes the password before saving

        if commit:
            user.save()  # Saves user data to the database if commit=True
        return user

# Profile Update Form (separate from RegistrationForm)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_picture']


