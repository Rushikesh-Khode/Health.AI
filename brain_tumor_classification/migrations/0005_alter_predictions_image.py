# Generated by Django 4.1 on 2023-02-19 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "brain_tumor_classification",
            "0004_predictions_glioma_predictions_meningioma_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="predictions",
            name="image",
            field=models.TextField(max_length=1048576),
        ),
    ]
