from django.contrib import admin
from .models import SiteContent


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