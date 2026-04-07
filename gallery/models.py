from django.db import models
from django.utils.text import slugify


class GalleryAlbum(models.Model):
    """Galereya albomlari"""
    title = models.CharField(max_length=300, verbose_name="Album nomi")
    slug = models.SlugField(max_length=350, unique=True, verbose_name="Slug")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    cover_image = models.ImageField(upload_to='gallery_covers/', null=True, blank=True, verbose_name="Muqova rasmi")
    event_date = models.DateField(null=True, blank=True, verbose_name="Tadbir sanasi")
    photos_count = models.PositiveIntegerField(default=0, verbose_name="Rasmlar soni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        db_table = 'gallery_albums'
        verbose_name = "Galereya albomi"
        verbose_name_plural = "Galereya albomlari"
        ordering = ['sort_order', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'sort_order']),
            models.Index(fields=['event_date']),
        ]

    def __str__(self):
        return self.title
    
    @property
    def cover_image_url(self):
        """Muqova rasm URL ni olish"""
        if self.cover_image:
            return self.cover_image.url
        return None
    
    def save(self, *args, **kwargs):
        """Slug avtomatik yaratish"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GalleryPhoto(models.Model):
    """Galereya rasmlari"""
    album = models.ForeignKey(
        GalleryAlbum,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Album"
    )
    image = models.ImageField(upload_to='gallery_photos/', verbose_name="Asosiy rasm")
    thumbnail = models.ImageField(upload_to='gallery_thumbnails/', verbose_name="Kichik rasm")
    caption = models.CharField(max_length=500, null=True, blank=True, verbose_name="Izoh")
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        db_table = 'gallery_photos'
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya rasmlari"
        ordering = ['sort_order', 'created_at']
        indexes = [
            models.Index(fields=['album', 'sort_order']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.album.title} - rasm #{self.pk}"
    
    @property
    def image_url(self):
        """Asosiy rasm URL ni olish"""
        if self.image:
            return self.image.url
        return None
    
    @property
    def thumbnail_url(self):
        """Kichik rasm URL ni olish"""
        if self.thumbnail:
            return self.thumbnail.url
        return None
    
    def save(self, *args, **kwargs):
        """Rasm yuklanganda albomning photos_count ni yangilash"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Yangi rasm qo'shilganda albomning rasmlar sonini oshirish
            self.album.photos_count = self.album.photos.count()
            self.album.save()


class UsefulLink(models.Model):
    """Foydali havolalar"""
    name = models.CharField(max_length=200, verbose_name="Nomi")
    url = models.URLField(max_length=500, verbose_name="Havola")
    logo = models.ImageField(upload_to='useful_links_logos/', null=True, blank=True, verbose_name="Logo rasm")
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name="Qisqa tavsif")
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        db_table = 'useful_links'
        verbose_name = "Foydali havola"
        verbose_name_plural = "Foydali havolalar"
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'sort_order']),
        ]

    def __str__(self):
        return self.name
    
    @property
    def logo_url(self):
        """Logo URL ni olish"""
        if self.logo:
            return self.logo.url
        return None
