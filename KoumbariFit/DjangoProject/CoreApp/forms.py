from django import forms
from django.contrib.auth.models import User

# User Login Form
class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")


# User Registration Form
class RegistrationForm(forms.ModelForm):
    # Password fields with password input widgets for security
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    class Meta:
        model = User  # Uses Django's built-in User model
        fields = ['username', 'email', 'password']  # Fields displayed in the form
        labels = {
            'username': 'Username',
            'email': 'Email Address'
        }

    def clean(self):
        """
        Custom validation to ensure that password and confirm_password match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")  # Raises an error if passwords don't match

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
