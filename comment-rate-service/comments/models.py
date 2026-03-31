from django.db import models


class CommentRate(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ("book", "Book"),
        ("cloth", "Cloth"),
    ]

    customer_id = models.PositiveIntegerField(help_text="FK to customer-service")
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default="book")
    product_id = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(
        help_text="Rating from 1 to 5",
    )
    comment = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["customer_id", "product_type", "product_id"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rating {self.rating}/5 by customer {self.customer_id} for {self.product_type} {self.product_id}"
