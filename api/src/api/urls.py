# src/api/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.task_list, name='api'),
    path('add/', views.tak_add, name='task_add'),
    path('update/<int:task_number>/', views.task_status_update,
         name='task_status_update'),
    path('delete/<int:task_number>/', views.delete_task, name='delete_task'),
    path('accounts/', include('allauth.urls')),
]
