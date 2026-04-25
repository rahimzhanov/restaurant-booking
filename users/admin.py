from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Регистрируем кастомную модель User в админке Django.
    UserAdmin — стандартный класс админки для пользователей,
    который даёт готовые поля, фильтры и поиск.
    """

    # Поля, которые показываем в списке пользователей
    list_display = ['email', 'first_name', 'phone', 'role', 'is_active', 'date_joined']

    # По каким полям можно искать
    search_fields = ['email', 'first_name', 'phone']

    # Фильтры справа
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']

    # Группировка полей при редактировании пользователя
    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'password')
        }),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name', 'phone')
        }),
        ('Права доступа', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'role'),
        }),
    )

    # Поля, по которым производится сортировка
    ordering = ['-date_joined']