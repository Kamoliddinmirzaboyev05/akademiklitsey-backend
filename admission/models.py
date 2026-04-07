from django.db import models


class AdmissionInfo(models.Model):
    """Qabul ma'lumotlari"""
    academic_year = models.CharField(max_length=20, verbose_name="O'quv yili")
    total_quota = models.PositiveIntegerField(verbose_name="Jami o'rinlar")
    grant_quota = models.PositiveIntegerField(verbose_name="Grant o'rinlari")
    contract_quota = models.PositiveIntegerField(verbose_name="Kontrakt o'rinlari")
    contract_price = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True,
        verbose_name="Kontrakt summasi (so'm)"
    )
    application_start = models.DateField(verbose_name="Ariza qabul boshlanishi")
    application_end = models.DateField(verbose_name="Ariza qabul tugashi")
    exam_date = models.DateField(null=True, blank=True, verbose_name="Imtihon sanasi")
    results_date = models.DateField(null=True, blank=True, verbose_name="Natijalar e'lon qilinish sanasi")
    online_apply_url = models.CharField(
        max_length=500, null=True, blank=True,
        verbose_name="Onlayn ariza havolasi"
    )
    is_active = models.BooleanField(default=True, verbose_name="Joriy yil ma'lumoti")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        db_table = 'admission_info'
        verbose_name = "Qabul ma'lumoti"
        verbose_name_plural = "Qabul ma'lumotlari"
        ordering = ['-academic_year']
        indexes = [
            models.Index(fields=['academic_year']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.academic_year} - Qabul"


class AdmissionSubject(models.Model):
    """Imtihon fanlari"""
    class SubjectType(models.TextChoices):
        TEST = 'test', 'Test'
        ESSAY = 'essay', 'Insho'
        INTERVIEW = 'interview', 'Intervyu'

    subject_name = models.CharField(max_length=200, verbose_name="Fan nomi")
    subject_type = models.CharField(
        max_length=20,
        choices=SubjectType.choices,
        default=SubjectType.TEST,
        verbose_name="Fan turi"
    )
    max_score = models.PositiveIntegerField(verbose_name="Maksimal ball")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'admission_subjects'
        verbose_name = "Imtihon fani"
        verbose_name_plural = "Imtihon fanlari"
        ordering = ['sort_order', 'subject_name']
        indexes = [
            models.Index(fields=['subject_type']),
            models.Index(fields=['sort_order']),
        ]

    def __str__(self):
        return self.subject_name


class AdmissionDocument(models.Model):
    """Talab qilinadigan hujjatlar"""
    document_name = models.CharField(max_length=300, verbose_name="Hujjat nomi")
    document_file = models.FileField(
        upload_to='admission_documents/',
        null=True, blank=True,
        verbose_name="Hujjat fayli"
    )
    is_required = models.BooleanField(default=True, verbose_name="Majburiy")
    note = models.CharField(
        max_length=500, null=True, blank=True,
        verbose_name="Izoh"
    )
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'admission_documents'
        verbose_name = "Talab qilinadigan hujjat"
        verbose_name_plural = "Talab qilinadigan hujjatlar"
        ordering = ['sort_order', 'document_name']
        indexes = [
            models.Index(fields=['is_required']),
            models.Index(fields=['sort_order']),
        ]

    def __str__(self):
        return self.document_name
    
    @property
    def document_file_url(self):
        """Fayl URL ni olish"""
        if self.document_file:
            return self.document_file.url
        return None


class FAQ(models.Model):
    """Ko'p so'raladigan savollar"""
    class Category(models.TextChoices):
        ADMISSION = 'admission', 'Qabul'
        GENERAL = 'general', 'Umumiy'
        EDUCATION = 'education', 'Ta\'lim'
        PAYMENT = 'payment', 'To\'lov'

    question = models.TextField(verbose_name="Savol matni")
    answer = models.TextField(verbose_name="Javob matni")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL,
        verbose_name="Kategoriya"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifaga chiqarish")
    sort_order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        db_table = 'faqs'
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ lar"
        ordering = ['sort_order', 'question']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['sort_order']),
        ]

    def __str__(self):
        return self.question[:100]