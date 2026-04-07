from django.contrib import admin
from .models import Circle


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'teacher', 'max_students', 'current_students', 'is_active', 'sort_order']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order', 'name']
    readonly_fields = ['slug']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('O\'qituvchi va o\'quvchilar', {
            'fields': ('teacher', 'max_students', 'current_students')
        }),
        ('Dars jadvali', {
            'fields': ('schedule', 'room')
        }),
        ('Media va sozlamalar', {
            'fields': ('photo', 'is_active', 'sort_order')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Yangi obyekt yaratilayotganda slug ni editable qilish"""
        if obj is None:
            return []
        return ['slug']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher')
