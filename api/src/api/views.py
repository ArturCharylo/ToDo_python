from rest_framework.views import APIView
from rest_framework.response import Response


class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello from API!"})


class ApiPage(APIView):
    def get(self, request):
        return Response({"message": "This is an API Endpoint!"})
