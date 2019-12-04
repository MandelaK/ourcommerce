from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import login_page, register_page, guest_register_page

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/guest/", guest_register_page, name="register_guest"),
]
