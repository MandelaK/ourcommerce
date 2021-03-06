"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cart.views import cart_home
from .views import home_page, contact_page, about_page


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("", home_page, name="home"),
    path("about/", about_page, name="about"),
    path("contact/", contact_page, name="contact"),
    path(
        "address/",
        include(("addresses.urls", "addresses"), namespace="addresses"),
        name="addresses",
    ),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("products/", include(("products.urls", "products"), namespace="products")),
    path("search/", include(("search.urls", "search"), namespace="search")),
    path("api/v1/auth/", include(("api.accounts.urls", "api-auth"))),
]

# don't serve static files in production
if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
