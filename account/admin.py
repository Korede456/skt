from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("full_name", "username", "password")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("full_name", "username", "password1", "password2"),
        }),
    )
    list_display = ("username", "full_name")
    search_fields = ("username", "full_name")
    ordering = ("username",)
