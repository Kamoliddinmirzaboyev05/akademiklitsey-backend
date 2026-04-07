from django.contrib import admin
from .models import News, Announcement, NewsImage, AnnouncementImage


class NewsImageInline(admin.TabularInline):
    """News uchun inline image rasm"""
    model = NewsImage
    extra = 0
    fields = ['image', 'caption', 'sort_order']
    ordering = ['sort_order']


class AnnouncementImageInline(admin.TabularInline):
    """Announcement uchun inline image rasm"""
    model = AnnouncementImage
    extra = 0
    fields = ['image', 'caption', 'sort_order']
    ordering = ['sort_order']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'views_count', 'published_at', 'created_by']
    list_filter = ['status', 'is_featured', 'published_at', 'created_at']
    search_fields = ['title', 'short_description']
    list_editable = ['status', 'is_featured']
    ordering = ['-published_at', '-created_at']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'slug']
    inlines = [NewsImageInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'short_description', 'content')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Nashr sozlamalari', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('views_count', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Yangi obyekt yaratilayotganda ba'zi fieldlarni editable qilish"""
        if obj is None:
            return ['views_count', 'created_at', 'updated_at']
        return ['views_count', 'created_at', 'updated_at', 'slug']
    
    def save_model(self, request, obj, form, change):
        """created_by ni avtomatik to'ldirish"""
        if not change:  # Yangi obyekt yaratilayotganda
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_important', 'expires_at', 'published_at', 'created_by']
    list_filter = ['status', 'is_important', 'published_at', 'expires_at']
    search_fields = ['title', 'short_description']
    list_editable = ['status', 'is_important']
    ordering = ['-published_at', '-created_at']
    readonly_fields = ['views_count', 'created_at', 'slug']
    inlines = [AnnouncementImageInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'short_description', 'content')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Nashr sozlamalari', {
            'fields': ('status', 'is_important', 'published_at', 'expires_at')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('views_count', 'created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Yangi obyekt yaratilayotganda ba'zi fieldlarni editable qilish"""
        if obj is None:
            return ['views_count', 'created_at']
        return ['views_count', 'created_at', 'slug']
    
    def save_model(self, request, obj, form, change):
        """created_by ni avtomatik to'ldirish"""
        if not change:  # Yangi obyekt yaratilayotganda
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['news', 'caption', 'sort_order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['news__title', 'caption']
    list_editable = ['sort_order']
    ordering = ['news', 'sort_order', 'created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('news')


@admin.register(AnnouncementImage)
class AnnouncementImageAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'caption', 'sort_order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['announcement__title', 'caption']
    list_editable = ['sort_order']
    ordering = ['announcement', 'sort_order', 'created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('announcement')
