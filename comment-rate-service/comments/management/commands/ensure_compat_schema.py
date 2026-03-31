from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Ensure comment-rate-service schema is compatible with product_type/product_id."

    def handle(self, *args, **options):
        statements = [
            "ALTER TABLE comments_commentrate ADD COLUMN IF NOT EXISTS product_type varchar(20) DEFAULT 'book'",
            "ALTER TABLE comments_commentrate ADD COLUMN IF NOT EXISTS product_id integer",
            "UPDATE comments_commentrate SET product_id = book_id WHERE product_id IS NULL",
            "ALTER TABLE comments_commentrate ALTER COLUMN product_type SET NOT NULL",
            "ALTER TABLE comments_commentrate ALTER COLUMN product_id SET NOT NULL",
            "ALTER TABLE comments_commentrate ALTER COLUMN book_id DROP NOT NULL",
            "CREATE UNIQUE INDEX IF NOT EXISTS comments_commentrate_customer_type_product_idx ON comments_commentrate(customer_id, product_type, product_id)",
        ]

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS("Comment schema compatibility ensured."))
