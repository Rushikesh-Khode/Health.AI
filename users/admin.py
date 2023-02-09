from django.contrib import admin

from users.models import User, Gender


@admin.register(User)
class User(admin.ModelAdmin):
    pass


@admin.register(Gender)
class Gender(admin.ModelAdmin):
    pass
