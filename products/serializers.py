from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description',
                  'created_at', 'product_count']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'description',
                  'category', 'category_detail', 'created_at']
        # These are auto-generated
        read_only_fields = ['id', 'slug', 'created_at']
