# Generated by Django 4.1 on 2023-02-11 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="x_auth_created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="x_auth_token",
            field=models.CharField(max_length=256, null=True),
        ),
    ]