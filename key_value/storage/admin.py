from django.contrib import admin

from .models import Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    readonly_fields = ["data", "created_at", "updated_at"]
    list_display = ("key", "value", "created_at", "updated_at", "id")

    def key(self, obj):
        return obj.data["key"]

    def value(self, obj):
        return obj.data["value"]
