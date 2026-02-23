from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Router automatically maps the standard RESTful URLs for the ViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# The API URLs are now fully handled by the router
urlpatterns = [
    path('', include(router.urls)),
]