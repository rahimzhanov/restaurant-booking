from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Админка для управления бронированиями.
    """

    list_display = [
        "id",
        "user",
        "table",
        "date",
        "time",
        "guests",
        "status",
        "created_at",
    ]
    list_filter = ["status", "date", "table"]
    search_fields = ["user__email", "user__first_name", "table__number"]
    date_hierarchy = "date"  # Удобная навигация по датам
    list_editable = ["status"]  # Меняем статус прямо в списке

    # Группировка полей при редактировании
    fieldsets = (
        (
            "Информация о бронировании",
            {"fields": ("user", "table", "date", "time", "duration", "guests")},
        ),
        ("Статус и комментарий", {"fields": ("status", "comment")}),
    )
