from django.contrib import admin
from .models import Statistic


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'key', 'value', 'sort_order', 'updated_at']
    list_filter = ['sort_order', 'updated_at']
    search_fields = ['label', 'key']
    ordering = ['sort_order', 'label']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('key', 'label', 'value')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('icon', 'sort_order')
        }),
    )
