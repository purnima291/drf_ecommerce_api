from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartSummarySerializer,
    CartItemSerializer,
    CartItemCreateSerializer
)
from products.models import Product


class CartAPIView(APIView):
    """
    Handle cart operations for authenticated users.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get user's current cart with all items"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)

        return Response({
            'success': True,
            'message': 'Cart retrieved successfully',
            'data': serializer.data
        })

    def delete(self, request):
        """Clear all items from cart"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # User has no cart, nothing to delete
            return Response({
                'success': True,
                'message': 'Cart is already empty - no cart exists',
                'data': {
                    'id': None,
                    'total_items': 0,
                    'total_price': '0.00',
                    'items': []
                }
            })

        if cart.items.count() == 0:
            return Response({
                'success': True,
                'message': 'Cart is already empty',
                'data': CartSerializer(cart).data
            })

        cart.clear()

        return Response({
            'success': True,
            'message': 'Cart cleared successfully',
            'data': CartSerializer(cart).data
        })


class AddToCartAPIView(APIView):
    """
    Add items to cart - handles both new items and quantity updates.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Add product to the cart or update quantity if already exists"""
        serializer = CartItemCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        product_slug = serializer.validated_data['product_slug']
        quantity = serializer.validated_data['quantity']

        # Get or create user cart
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Get the product
        product = get_object_or_404(Product, slug=product_slug)

        # Use database transaction for consistency
        with transaction.atomic():
            # Check if item already exists in cart
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price': product.price  # Lock the price
                }
            )

            if not item_created:
                # Item already exists, add to existing quantity
                cart_item.quantity += quantity
                cart_item.save()
                message = f'Updated {product.name} quantity in cart'
            else:
                # New item added
                message = f"Added {product.name} to cart"

        
        # Return updated cart item

        return Response({
            'success': True,
            'message': message,
            'data': {
                'cart_item': CartItemSerializer(cart_item).data,
                'cart_summary': CartSummarySerializer(cart).data
            }
        }, status=status.HTTP_201_CREATED if item_created else status.HTTP_200_OK)
    

class CartItemAPIView(APIView):
    """
    Handle individual cart item operations (update quantity, remove quantity)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_cart_item(self, request, item_id):
        """Helper method to get cart item belonging to current user"""
        return get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
    
    def put(self, request, item_id):
        """Update cart item quantity"""
        cart_item = self.get_cart_item(request, item_id)

        # Get new quantity from request
        new_quantity = request.data.get('quantity')

        if new_quantity is None:
            return Response({
                'success': False,
                'message': 'Quantity is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_quantity = int(new_quantity)
        except (ValueError, TypeError):
            return Response({
                'success': False,
                'message': 'Quantity must be a valid integer'
            }, status=status.HTTP_400_BAD_REQUEST)

        if new_quantity < 0:
            return Response({
                'success': False,
                'message': 'Quantity cannot be negative',
            }, status=status.HTTP_400_BAD_REQUEST) 

        # Update quantity
        old_quantity = cart_item.quantity
        cart_item.update_quantity(new_quantity)

        # Get updated cart item (might be deleted if quantity was 0)
        try:
            updated_item = CartItem.objects.get(id=item_id)
            serializer = CartItemSerializer(updated_item)
            message = f'Updated quantity from {old_quantity} to {new_quantity}'
        except CartItem.DoesNotExist:
            # Item was deleted due to 0 quantity
            serializer = None
            message = 'Item removed from cart'

        return Response({
            'success': True,
            'message': message,
            'data': serializer.data if serializer else None
        })

    def delete(self, request, item_id):
        """Remove item from cart"""
        cart_item = self.get_cart_item(request, item_id)
        product_name = cart_item.product.name

        cart_item.delete()

        return Response({
            'success': True,
            'message': f'Removed {product_name} from cart'
        }, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cart_summary(request):
    """
    Get lightweight cart summary for navigation bars, etc.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSummarySerializer(cart)

    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


