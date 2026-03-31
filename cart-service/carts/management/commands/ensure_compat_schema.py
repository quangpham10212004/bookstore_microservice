from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Ensure cart-service schema is compatible with product_type/product_id."

    def handle(self, *args, **options):
        statements = [
            "ALTER TABLE carts_cartitem ADD COLUMN IF NOT EXISTS product_type varchar(20) DEFAULT 'book'",
            "ALTER TABLE carts_cartitem ADD COLUMN IF NOT EXISTS product_id integer",
            "UPDATE carts_cartitem SET product_id = book_id WHERE product_id IS NULL",
            "ALTER TABLE carts_cartitem ALTER COLUMN product_type SET NOT NULL",
            "ALTER TABLE carts_cartitem ALTER COLUMN product_id SET NOT NULL",
            "ALTER TABLE carts_cartitem ALTER COLUMN book_id DROP NOT NULL",
            "CREATE UNIQUE INDEX IF NOT EXISTS carts_cartitem_cart_type_product_idx ON carts_cartitem(cart_id, product_type, product_id)",
        ]

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS("Cart schema compatibility ensured."))
