from django.db import models


class Cloth(models.Model):
    name = models.CharField(max_length=300)
    brand = models.CharField(max_length=200)
    sku = models.CharField(max_length=32, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    catalog_id = models.PositiveIntegerField(help_text="FK to catalog-service")
    description = models.TextField(blank=True, default="")
    image_url = models.URLField(blank=True, default="")
    size_label = models.CharField(max_length=50, blank=True, default="")
    color = models.CharField(max_length=100, blank=True, default="")
    material = models.CharField(max_length=150, blank=True, default="")
    gender = models.CharField(max_length=50, blank=True, default="")
    created_by_staff_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.brand}"
