from django.contrib import admin
from .models import Predictions


@admin.register(Predictions)
class Predictions(admin.ModelAdmin):
    pass
