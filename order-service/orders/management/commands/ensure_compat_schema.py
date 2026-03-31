from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Ensure order-service schema is compatible with product_type/product_id."

    def handle(self, *args, **options):
        statements = [
            "ALTER TABLE orders_orderitem ADD COLUMN IF NOT EXISTS product_type varchar(20) DEFAULT 'book'",
            "ALTER TABLE orders_orderitem ADD COLUMN IF NOT EXISTS product_id integer",
            "UPDATE orders_orderitem SET product_id = book_id WHERE product_id IS NULL",
            "ALTER TABLE orders_orderitem ALTER COLUMN product_type SET NOT NULL",
            "ALTER TABLE orders_orderitem ALTER COLUMN product_id SET NOT NULL",
            "ALTER TABLE orders_orderitem ALTER COLUMN book_id DROP NOT NULL",
        ]

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS("Order schema compatibility ensured."))
