from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Main cart operations
    path('', views.CartAPIView.as_view(), name='cart-detail'), # GET, DELETE

    # Add items to cart
    path('add/', views.AddToCartAPIView.as_view(), name='add-to-cart'), # POST

    # Individual cart item operations
    path('items/<int:item_id>/', views.CartItemAPIView.as_view(), name='cart-item-detail'), # PUT, DELETE

    # Cart summary (lightweight)
    path('summary/', views.cart_summary, name='cart-summary') # GET
]