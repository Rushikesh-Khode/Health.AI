# Generated by Django 4.1 on 2023-02-09 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_gender_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.IntegerField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
    ]
