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


def get_unique_username(base_username):
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1
    return username


@api_view(['POST'])
def github_login(request):
    code = request.data.get('code')
    if not code:
        return Response({"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Exchange code for access_token
    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_CLIENT,
            "client_secret": settings.GITHUB_SECRET,
            "code": code,
            "redirect_uri": "http://localhost:5173/github-callback"
        }
    )

    if token_res.status_code != 200:
        return Response({"error": "Failed to fetch token"}, status=status.HTTP_400_BAD_REQUEST)

    token_json = token_res.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return Response({"error": "No access token in response"}, status=status.HTTP_400_BAD_REQUEST)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json"
    }

    # 2. Get user data from Github
    user_res = requests.get("https://api.github.com/user", headers=headers)
    email_res = requests.get(
        "https://api.github.com/user/emails", headers=headers)

    if user_res.status_code != 200 or email_res.status_code != 200:
        return Response({"error": "Failed to fetch user info"}, status=status.HTTP_400_BAD_REQUEST)

    github_user = user_res.json()
    emails = email_res.json()

    primary_email = next((e["email"]
                         for e in emails if e.get("primary")), None)
    if not primary_email:
        return Response({"error": "No primary email found"}, status=status.HTTP_400_BAD_REQUEST)

    # 3. Check if user exists
    user = User.objects.filter(email=primary_email).first()
    if user:
        # If exists refresh JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        }, status=200)

    # 4. Create new user with unique username
    username = get_unique_username(github_user.get("login", primary_email))
    user = User.objects.create(
        email=primary_email,
        username=username
    )

    # 5. Generate JWT
    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": UserSerializer(user).data
    }, status=200)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def users_list(request):
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
