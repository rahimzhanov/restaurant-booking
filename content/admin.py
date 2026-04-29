from django.contrib import admin
from .models import SiteContent, ContactMessage


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['section', 'title', 'updated_at']
    list_filter = ['section']
    search_fields = ['title', 'content']
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Раздел', {
            'fields': ('section',)
        }),
        ('Содержание', {
            'fields': ('title', 'content')
        }),
        ('Служебное', {
            'fields': ('updated_at',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']