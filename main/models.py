from django.db import models


class Statistic(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Kalit"
    )

    value = models.PositiveIntegerField(
        default=0,
        verbose_name="Qiymat"
    )

    label = models.CharField(
        max_length=100,
        verbose_name="Yorliq (frontendda chiqadigan matn)"
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Icon classi"
    )

    sort_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Tartib"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Statistika"
        verbose_name_plural = "Statistikalar"
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.label} - {self.value}"
