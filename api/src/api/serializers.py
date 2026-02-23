from rest_framework import serializers
from .models import Task

# Serializer that automatically handles converting Task instances to JSON and vice-versa
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'