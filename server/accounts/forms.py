from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
    """Define the login form"""
    email = forms.CharField(
        label='Email', widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your email..."}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password..."})
    )


class GuestForm(forms.Form):
    """Define the form for guest users"""
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email..."})
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
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm your password..."})
    )

    def clean_username(self):
        """Ensure usernames are unique"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "A user with this username exists already"
            )
        return username

    def clean_email(self):
        """Ensure usernames are unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with this email exists already"
            )
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password != password2:
            raise forms.ValidationError("Passwords must match!")
        return data
