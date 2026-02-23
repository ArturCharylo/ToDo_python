from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

# ModelViewSet automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('task_number')
    serializer_class = TaskSerializer