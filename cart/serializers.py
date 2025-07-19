from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual cart items.
    Includes nested product data and calculated totals.
    """
    # Read only field with product information
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_description = serializers.CharField(source='product.description', read_only=True)

    # Calculated fields
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_slug',
            'product_description',
            'quantity',
            'price',
            'total_price',
            'added_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'price', 'added_at', 'updated_at']

    def validate_quantity(self, value):
        """Ensure quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    

class CartItemCreateSerializer(serializers.Serializer):
    """
    Simplified serializer for adding items to cart.
    Only requires product and quantity.
    """
    product_slug = serializers.CharField()
    quantity = serializers.IntegerField(default=1)

    def validate_quantity(self, value):
        """Ensure qunatity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    
    def validate_product_slug(self, value):
        """Ensure product exists"""
        from products.models import Product
        try:
            Product.objects.get(slug=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found')
        return value
    
class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the complete shopping cart.
    Include all cart items and calculated totals.
    """
    items = CartItemSerializer(many=True, read_only=True)

    # Calculated fields
    total_items = serializers.IntegerField(read_only=True)
    total_price =serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    # User information
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'user_name',
            'items',
            'total_items',
            'total_price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class CartSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for cart summary (without full item details).
    Useful for navigation bars, quick checks, etc.
    """
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            'id',
            'total_items',
            'total_price',
            'updated_at'
        ]