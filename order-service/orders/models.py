from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    customer_id = models.PositiveIntegerField(help_text="FK to customer-service")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=50, blank=True, default="")
    shipping_method = models.CharField(max_length=50, blank=True, default="")
    shipping_address = models.TextField(blank=True, default="")
    payment_id = models.PositiveIntegerField(null=True, blank=True)
    shipping_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ("book", "Book"),
        ("cloth", "Cloth"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default="book")
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem(order={self.order_id}, type={self.product_type}, product={self.product_id})"
