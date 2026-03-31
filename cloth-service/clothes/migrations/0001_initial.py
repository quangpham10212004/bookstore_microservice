from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cloth",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=300)),
                ("brand", models.CharField(max_length=200)),
                ("sku", models.CharField(max_length=32, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.PositiveIntegerField(default=0)),
                ("catalog_id", models.PositiveIntegerField(help_text="FK to catalog-service")),
                ("description", models.TextField(blank=True, default="")),
                ("image_url", models.URLField(blank=True, default="")),
                ("size_label", models.CharField(blank=True, default="", max_length=50)),
                ("color", models.CharField(blank=True, default="", max_length=100)),
                ("material", models.CharField(blank=True, default="", max_length=150)),
                ("gender", models.CharField(blank=True, default="", max_length=50)),
                ("created_by_staff_id", models.PositiveIntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
