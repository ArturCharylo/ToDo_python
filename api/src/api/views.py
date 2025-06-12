from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = ProductSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def tak_add(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
