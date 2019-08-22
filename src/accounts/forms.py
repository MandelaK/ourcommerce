from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
    """Define the login form"""
    username = forms.CharField(
        label='Username', widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username..."}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password..."})
    )


class RegisterForm(forms.Form):
    """Define the registration form"""

    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email..."})
    )
    username = forms.CharField(
        label='Username', widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username..."}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password..."})
    )
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm your password..."})
    )

    def clean_username(self):
        """Ensure usernames are unique"""
        username = self.cleaned_data.get('username')
        query = User.objects.filter(username=username)
        if query.exists():
            raise forms.ValidationError(
                "A user with this username exists already"
            )
        return username

    def clean_email(self):
        """Ensure usernames are unique"""
        email = self.cleaned_data.get('email')
        query = User.objects.filter(email=email)
        if query.exists():
            raise forms.ValidationError(
                "A user with this email exists already"
            )
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match!")
        return data
