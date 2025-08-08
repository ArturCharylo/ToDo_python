# src/api/urls.py
from django.urls import path, include
from . import views
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.views import APIView
from rest_framework.response import Response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


urlpatterns = [
    path('', views.task_list, name='api'),
    path('add/', views.task_add, name='task_add'),
    path('update/<int:task_number>/', views.task_status_update,
         name='task_status_update'),
    path('delete/<int:task_number>/', views.delete_task, name='delete_task'),
    path('add_user/', views.add_credencials, name='add_credencials'),
    path('get_users', views.users_list, name="users_list"),
    path('accounts/', include('allauth.urls')),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path('github/login/', views.github_login, name='github_login'),
]
