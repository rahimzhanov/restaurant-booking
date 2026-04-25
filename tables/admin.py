from django.contrib import admin

from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """
    Админка для управления столиками.
    """

    list_display = ["number", "seats", "location", "is_active"]
    list_filter = ["is_active", "seats"]
    search_fields = ["number", "location"]
    list_editable = ["is_active"]  # Можно менять активность прямо в списке
