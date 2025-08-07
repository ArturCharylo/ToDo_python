from .serializers import TaskSerializer, UserSerializer
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.conf import settings
from .models import Task, User
from dotenv import load_dotenv
import os
load_dotenv('./.env')


class GitHubLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "Brak kodu OAuth"}, status=400)

        # 1. Wymiana code na access_token
        token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": os.getenv("GITHUB_CLIENT"),
                "client_secret": os.getenv("GITHUB_SECRET"),
                "code": code,
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "Nie udało się pobrać access tokena"}, status=400)

        # 2. Pobierz dane użytkownika z GitHub
        user_response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        user_data = user_response.json()
        email = user_data.get("email") or f'{user_data["id"]}@github.com'
        username = user_data.get("login")

        # 3. Stwórz użytkownika jeśli nie istnieje
        user, _ = User.objects.get_or_create(
            email=email, defaults={"username": username})

        # 4. Generuj JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                "username": user.username
            }
        })


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
