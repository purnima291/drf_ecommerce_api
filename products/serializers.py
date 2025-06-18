from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'description', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at'] # These are auto-generated

