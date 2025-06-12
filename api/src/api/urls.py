# src/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='api'),
    path('add/', views.tak_add, name='task_add'),
    path('update/<int:task_id>/', views.task_status_update,
         name='task_status_update'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
