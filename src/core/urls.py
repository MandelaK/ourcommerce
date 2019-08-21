from django.urls import path
from .views import home_page, contact_page, about_page, login_page, register_page, logout

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout, name='logout')
]
