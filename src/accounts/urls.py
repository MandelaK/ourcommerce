from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import login_page, register_page, logout

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
