from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from accounts.forms import LoginForm, RegisterForm


def login_page(request):
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
            # we clear the form
            context['form'] = LoginForm()
            if is_safe_url(redirect_path, request.get_host()):
                print(f"redirectin to {redirect_path}")
                return redirect(redirect_path)
            return redirect('/')

        else:
            pass

    return render(request, 'accounts/login.html', context)


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
