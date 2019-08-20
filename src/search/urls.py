from django.urls import path
from search.views import SearchProductView

urlpatterns = [
    path('', SearchProductView.as_view(), name='query'),
]
