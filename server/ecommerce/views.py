from django.shortcuts import render, redirect
from .forms import ContactForm


def home_page(request):
    context = {"title": "Welcome to OurCommerce", "content": "OurCommerce"}
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    context = {
        "title": "Contact Us",
        "content": "Get in touch with us!",
        "form": contact_form,
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, "contact_page.html", context)


def about_page(request):
    context = {"title": "About Us", "content": "Here's everything we are about..."}
    return render(request, "about_page.html", context)
