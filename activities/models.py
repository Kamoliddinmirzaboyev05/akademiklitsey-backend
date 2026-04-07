from django.db import models
from django.utils.text import slugify


class Circle(models.Model):
    class Category(models.TextChoices):
        SPORT = 'sport', 'Sport'
        ART = 'art', 'San\'at'
        SCIENCE = 'science', 'Fan'
        LANGUAGE = 'language', 'Til'
        TECH = 'tech', 'Texnologiya'
        OTHER = 'other', 'Boshqa'

    name = models.CharField(max_length=200, verbose_name="To'garak nomi")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Slug")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name="Kategoriya"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    teacher = models.ForeignKey(
        'structure.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='circles',
        verbose_name="Rahbar o'qituvchi"
    )
    max_students = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Maksimal o'rinlar"
    )
    current_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Hozirgi o'quvchilar soni"
    )
    schedule = models.CharField(
        max_length=300,
        null=True, blank=True,
        verbose_name="Dars vaqti"
    )
    room = models.CharField(max_length=50, null=True, blank=True, verbose_name="Xona")
    photo = models.ImageField(upload_to='circles/', null=True, blank=True, verbose_name="Rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'circles'
        verbose_name = "To'garak"
        verbose_name_plural = "To'garaklar"
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_active', 'sort_order']),
        ]

    def __str__(self):
        return self.name

    @property
    def available_slots(self):
        """Bo'sh o'rinlar soni"""
        if self.max_students is None:
            return None
        return max(0, self.max_students - self.current_students)

    @property
    def is_full(self):
        """To'garak to'lganmi"""
        if self.max_students is None:
            return False
        return self.current_students >= self.max_students

    def save(self, *args, **kwargs):
        """Slug avtomatik yaratish"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def photo_url(self):
        """Rasm URL ni olish"""
        if self.photo:
            return self.photo.url
        return None
