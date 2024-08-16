from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import User, UserAdminChangeForm, UserAdminCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ["username", "first_name", "last_name", "is_admin"]
    list_filter = ["is_admin", "is_active"]

    fieldsets = [
        ("Identifire", {"fields": ["username", "password"]}),
        (
            "Personal Information",
            {
                "fields": [
                    "first_name",
                    "last_name",
                ]
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_admin",
                    "is_superuser",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password", "password_confirm"],
            },
        ),
    ]
    search_fields = [
        "username",
    ]
    ordering = ["username"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
