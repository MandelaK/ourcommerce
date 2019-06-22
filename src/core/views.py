from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from core.forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
    context = {
        "title": "Welcome to OurCommerce",
        "content": "Are you ready to trade??"
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    context = {"title": "Contact Us",
               "content": "Get in touch with us!",
               "form": contact_form
               }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact_page.html', context)


def about_page(request):
    context = {"title": "About Us",
               "content": "Here's everything we are about..."}
    return render(request, 'about_page.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            # we clear the form
            context['form'] = LoginForm()
            return redirect('/')

        else:
            print("Error")

    return render(request, 'auth/login.html', context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(
            username=username, email=email, password=password)
        context['form'] = RegisterForm()

    return render(request, 'auth/register.html', context)
