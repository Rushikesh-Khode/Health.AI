# Generated by Django 4.1 on 2023-02-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
