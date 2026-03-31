from django.db import models


class Cart(models.Model):
    customer_id = models.PositiveIntegerField(unique=True, help_text="FK to customer-service")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for customer {self.customer_id}"


class CartItem(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ("book", "Book"),
        ("cloth", "Cloth"),
    ]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default="book")
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["cart", "product_type", "product_id"]

    def __str__(self):
        return f"CartItem(cart={self.cart_id}, type={self.product_type}, product={self.product_id}, qty={self.quantity})"
