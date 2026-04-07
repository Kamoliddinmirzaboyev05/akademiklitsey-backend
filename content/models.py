from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class News(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'published', 'Published'
        DRAFT = 'draft', 'Draft'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=350, unique=True, verbose_name="Slug")
    short_description = models.TextField(verbose_name="Qisqa tavsif")
    content = models.TextField(verbose_name="To'liq matn")
    thumbnail = models.CharField(max_length=500, blank=True, null=True, verbose_name="Asosiy rasm URL")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Holat"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifaga chiqarish")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Nashr sanasi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_created',
        verbose_name="Kim qo'shgan"
    )

    class Meta:
        db_table = 'news'
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['slug']),
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title

    def increment_views(self):
        """Ko'rishlar sonini +1 oshirish"""
        News.objects.filter(pk=self.pk).update(views_count=models.F('views_count') + 1)


class NewsImage(models.Model):
    """Yangilik rasmlari"""
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Yangilik"
    )
    image = models.ImageField(upload_to='news_images/', verbose_name="Rasm")
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name="Rasm izohi")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        db_table = 'news_images'
        verbose_name = "Yangilik rasmi"
        verbose_name_plural = "Yangilik rasmlari"
        ordering = ['sort_order', 'created_at']
        indexes = [
            models.Index(fields=['news', 'sort_order']),
        ]

    def __str__(self):
        return f"{self.news.title} - rasm #{self.pk}"
    
    @property
    def image_url(self):
        """Rasm URL ni olish"""
        if self.image:
            return self.image.url
        return None


class Announcement(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'published', 'Published'
        DRAFT = 'draft', 'Draft'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=350, unique=True, verbose_name="Slug")
    short_description = models.TextField(verbose_name="Qisqa tavsif")
    content = models.TextField(verbose_name="To'liq matn")
    thumbnail = models.CharField(max_length=500, blank=True, null=True, verbose_name="Rasm URL")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    is_important = models.BooleanField(default=False, verbose_name="Muhim e'lon")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Holat"
    )
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Muddati tugash sanasi")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Nashr sanasi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements_created',
        verbose_name="Kim qo'shgan"
    )

    class Meta:
        db_table = 'announcements'
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'is_important']),
            models.Index(fields=['slug']),
            models.Index(fields=['-published_at']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        """E'lon muddati tugaganligini tekshirish"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class AnnouncementImage(models.Model):
    """E'lon rasmlari"""
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="E'lon"
    )
    image = models.ImageField(upload_to='announcement_images/', verbose_name="Rasm")
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name="Rasm izohi")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        db_table = 'announcement_images'
        verbose_name = "E'lon rasmi"
        verbose_name_plural = "E'lon rasmlari"
        ordering = ['sort_order', 'created_at']
        indexes = [
            models.Index(fields=['announcement', 'sort_order']),
        ]

    def __str__(self):
        return f"{self.announcement.title} - rasm #{self.pk}"
    
    @property
    def image_url(self):
        """Rasm URL ni olish"""
        if self.image:
            return self.image.url
        return None