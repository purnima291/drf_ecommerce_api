from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator


class Cart(models.Model):
    """
    Shopping cart for authenticated users.
    One cart per user = simple and clean.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

    def __str__(self):
        return f'Cart for {self.user.username}'

    @property
    def total_items(self):
        """
        Total number of items in cart (sum of all quantities)
        """
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Total price of all items in cart"""
        return sum(item.total_price for item in self.items.all())

    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """
    Individual items in a shopping cart.
    Stores price at time of adding (price lock for customer protection)
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price when item was added to cart (locked price)'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        """Total price for this cart item (quantity * locked price)"""
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        """Auto-set price from product if not provided (price lock)"""
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

        # Update cart's updated_at timestamp
        self.cart.save()

    def update_quantity(self, new_quantity):
        """Update quantity with validation"""
        if new_quantity <= 0:
            self.delete()
        else:
            self.quantity = new_quantity
            self.save()