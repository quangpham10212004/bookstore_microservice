from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(
                    model_name="commentrate",
                    name="book_id",
                ),
            ],
        ),
    ]
