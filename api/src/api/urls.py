# src/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiPage.as_view(), name='api'),
]
