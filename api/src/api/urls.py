# src/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiPage.as_view(), name='api'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]
