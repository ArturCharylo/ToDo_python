# shop/serializers.py
from rest_framework import serializers
from .models import Task


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
