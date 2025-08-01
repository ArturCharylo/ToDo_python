from .serializers import TaskSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import Task, User


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def users_list(response):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def task_add(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def add_credencials(request):
    email = request.data.get('email')
    username = request.data.get('username')

    # Check if user already exists
    user = User.objects.filter(email=email).first(
    ) or User.objects.filter(username=username).first()

    if user:
        # User already exists, return 200
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    # If there is no user with that data, create one
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['Patch'])
def task_status_update(request, task_number):
    try:
        task = Task.objects.get(task_number=task_number)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.error, status=400)


@api_view(['DELETE'])
def delete_task(request, task_number):
    try:
        task = Task.objects.get(task_number=task_number)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    task.delete()
    return Response(status=204)
