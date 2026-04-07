from django.contrib import admin
from .models import Department, Teacher, Management


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_teacher', 'teachers_count', 'room_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['sort_order', 'name']
    readonly_fields = ['created_at', 'teachers_count']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'description', 'head_teacher')
        }),
        ('Kafedra ma\'lumotlari', {
            'fields': ('subjects', 'room_number', 'phone', 'email')
        }),
        ('Sozlamalar', {
            'fields': ('sort_order', 'is_active')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('created_at', 'teachers_count'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Yangi obyekt yaratilayotganda ba'zi fieldlarni editable qilish"""
        if obj is None:
            return ['created_at', 'teachers_count']
        return ['created_at', 'teachers_count']
    
    def teachers_count(self, obj):
        """Kafedradagi o'qituvchilar soni"""
        return obj.teachers_count
    teachers_count.short_description = 'O\'qituvchilar soni'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'department', 'category', 'experience_years', 'email', 'is_active']
    list_filter = ['category', 'department', 'is_active', 'created_at']
    search_fields = ['full_name', 'position', 'subject']
    list_editable = ['is_active', 'category']
    ordering = ['sort_order', 'full_name']
    readonly_fields = ['created_at', 'slug']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('full_name', 'slug', 'position', 'department')
        }),
        ('Ilmiy ma\'lumotlar', {
            'fields': ('academic_degree', 'academic_rank', 'category', 'experience_years')
        }),
        ('Ish ma\'lumotlari', {
            'fields': ('subject', 'email', 'photo')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('bio', 'achievements')
        }),
        ('Sozlamalar', {
            'fields': ('sort_order', 'is_active')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Yangi obyekt yaratilayotganda slug ni editable qilish"""
        if obj is None:
            return ['created_at']
        return ['created_at', 'slug']


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'academic_degree', 'phone', 'email', 'sort_order', 'is_active']
    list_filter = ['is_active', 'academic_degree']
    search_fields = ['full_name', 'position']
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('full_name', 'position', 'academic_degree')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('phone', 'email', 'reception_hours')
        }),
        ('Media va boshqa', {
            'fields': ('photo', 'bio')
        }),
        ('Sozlamalar', {
            'fields': ('sort_order', 'is_active')
        }),
    )
