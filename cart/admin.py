from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    """
    Inline editing of cart items within the cart admin page.
    Allows viewing and editing all cart items in one place.
    """
    model = CartItem
    extra = 0 # Don't show extra emplty forms
    readonly_fields = ('added_at', 'updated_at', 'total_price')
    fields = ('product', 'quantity', 'price', 'total_price', 'added_at')

    def total_price(self, obj):
        """Display calculated total price for each item"""
        if obj.id and obj.price is not None:
            return f'${obj.total_price:.2f}'
        elif obj.product and obj.quantity:
            # For new items, show what the total would be
            estimated_total = obj.quantity * obj.product.price
            return f'${estimated_total:.2f} (esitmated)'
        return '-'
    total_price.short_description = "Total Price"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin interface for managing shopping carts.
    """
    list_display = [
        'user', 
        'total_items_display', 
        'total_price_display', 
        'created_at', 
        'updated_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_items_display', 'total_price_display']

    # Show cart items inline
    inline = [CartItemInline]

    # Custom display methods
    def total_items_display(self, obj):
        """Dispaly total number of items in cart"""
        return obj.total_items
    total_items_display.short_description = "Total Items"

    def total_price_display(self, obj):
        """Display total cart value with currency formatting"""
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = "Total Value"

    # Optimise database queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin interface for individual cart items.
    Useful for detailed cart item management.
    """
    list_display = [
        'cart_user',
        'product',
        'quantity',
        'price',
        'total_price_display',
        'added_at'
    ]
    list_filter = [
        'added_at',
        'updated_at',
        'cart__user' # Filter by cart owner
    ]
    search_fields = [
        'cart__user__username',
        'product__name',
        'product__slug'
    ]
    readonly_fields = ['added_at', 'updated_at', 'total_price_display']

    # Custom display methods
    def cart_user(self, obj):
        """Display the cart owner's username"""
        return obj.cart.user.username
    cart_user.short_description = "Cart Owner"

    def total_price_display(self, obj):
        """Display total price for this cart item"""
        return f'${obj.total_price:.2f}'
    total_price_display.short_description = "Total Price"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'cart__user',
            'product'
        )
    
    # Organize field in the edit form
    fieldsets = (
        (
            'Cart Item Details', {
                'fields': ('cart', 'product', 'quantity')
            }
        ),
        (
            'Auto-calculated Values', {
                'fields': ('price', 'total_price_display',),
                'classes': ('collapse',),
                'description': 'Price is automatically set from the selected product'
            }
        ),
        (
            'Timestamps', {
                'fields': ('added_at', 'updated_at'),
                'classes': ('collapse',)
            }
        )
    )


# Optional: Customize admin site header
admin.site.site_header = 'E-commerce Admin'
admin.site.site_title = 'E-commerce Admin Portal'
admin.site.index_title = 'Welcome to E-commerce Administration'