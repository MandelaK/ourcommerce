from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail


def login_page(request):
    """
    Handle logic for the login view
    """
    form = LoginForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # delete guest email id if users log in
            try:
                del request.session['guest_email_id']
            except KeyError:
                pass
            # we clear the form
            context['form'] = LoginForm()
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect('/')

        else:
            pass

    return render(request, 'accounts/login.html', context)


def guest_register_page(request):
    """
    Handle logic for allowing guest users to checkout
    """
    form = GuestForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    context = {
        "form": form
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.pk
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        return redirect('auth/register/')

    return render(request, 'auth/register/', context)


User = get_user_model()


def logout(request):
    request.session.flush()
    return redirect('/')


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(
            username=username, email=email, password=password)
        context['form'] = RegisterForm()

    return render(request, 'accounts/register.html', context)
