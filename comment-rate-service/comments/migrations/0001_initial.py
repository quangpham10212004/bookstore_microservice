from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CommentRate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_id", models.PositiveIntegerField(help_text="FK to customer-service")),
                ("book_id", models.PositiveIntegerField(blank=True, help_text="Legacy FK to book-service", null=True)),
                ("product_type", models.CharField(choices=[("book", "Book"), ("cloth", "Cloth")], default="book", max_length=20)),
                ("product_id", models.PositiveIntegerField()),
                ("rating", models.PositiveIntegerField(help_text="Rating from 1 to 5")),
                ("comment", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("customer_id", "product_type", "product_id")},
            },
        ),
    ]
