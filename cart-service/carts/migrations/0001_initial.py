from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_id", models.PositiveIntegerField(help_text="FK to customer-service", unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("book_id", models.PositiveIntegerField(blank=True, help_text="Legacy FK to book-service", null=True)),
                ("product_type", models.CharField(choices=[("book", "Book"), ("cloth", "Cloth")], default="book", max_length=20)),
                ("product_id", models.PositiveIntegerField()),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("cart", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="carts.cart")),
            ],
            options={"unique_together": {("cart", "product_type", "product_id")}},
        ),
    ]
