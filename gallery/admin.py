from django.contrib import admin
from .models import GalleryAlbum, GalleryPhoto, UsefulLink


class GalleryPhotoInline(admin.TabularInline):
    """Gallery albomi ichida inline rasmlar"""
    model = GalleryPhoto
    extra = 0
    fields = ['image', 'thumbnail', 'caption', 'sort_order']
    ordering = ['sort_order']


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'photos_count', 'event_date', 'is_active', 'sort_order']
    list_filter = ['is_active', 'event_date']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order', '-created_at']
    readonly_fields = ['photos_count', 'created_at', 'updated_at', 'slug']
    inlines = [GalleryPhotoInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Tadbir', {
            'fields': ('event_date',)
        }),
        ('Sozlamalar', {
            'fields': ('is_active', 'sort_order')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('photos_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Yangi obyekt yaratilayotganda slug ni editable qilish"""
        if obj is None:
            return ['photos_count', 'created_at', 'updated_at']
        return ['photos_count', 'created_at', 'updated_at', 'slug']
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('photos')


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['album', 'caption', 'sort_order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['caption']
    list_editable = ['sort_order']
    ordering = ['album', 'sort_order', 'created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('album')


@admin.register(UsefulLink)
class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active', 'sort_order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order', 'name']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'url', 'description')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Sozlamalar', {
            'fields': ('is_active', 'sort_order')
        }),
    )
