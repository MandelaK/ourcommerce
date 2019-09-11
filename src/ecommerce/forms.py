from django import forms


class ContactForm(forms.Form):
    """Define the contact form information"""
    full_name = forms.CharField(label='Full Names', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Your full names"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Your email"}))
    content = forms.CharField(
        label='Content', widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your message"}))
