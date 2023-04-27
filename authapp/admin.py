from django.contrib import admin
from authapp import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name",
                    "address", "phone", "user", "session_id"]
