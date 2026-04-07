from django.contrib import admin
from .models import AdmissionInfo, AdmissionSubject, AdmissionDocument, FAQ


@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'total_quota', 'grant_quota', 'contract_quota', 'contract_price', 'is_active']
    list_filter = ['is_active', 'academic_year']
    search_fields = ['academic_year']
    list_editable = ['is_active']
    ordering = ['-academic_year']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('academic_year', 'is_active')
        }),
        ('Kvotalar', {
            'fields': ('total_quota', 'grant_quota', 'contract_quota', 'contract_price')
        }),
        ('Sanalar', {
            'fields': ('application_start', 'application_end', 'exam_date', 'results_date')
        }),
        ('Qo\'shimcha', {
            'fields': ('online_apply_url',)
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdmissionSubject)
class AdmissionSubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_type', 'max_score', 'sort_order']
    list_filter = ['subject_type']
    search_fields = ['subject_name', 'description']
    list_editable = ['sort_order']
    ordering = ['sort_order', 'subject_name']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('subject_name', 'subject_type', 'max_score')
        }),
        ('Qo\'shimcha', {
            'fields': ('description', 'sort_order')
        }),
    )


@admin.register(AdmissionDocument)
class AdmissionDocumentAdmin(admin.ModelAdmin):
    list_display = ['document_name', 'is_required', 'sort_order']
    list_filter = ['is_required']
    search_fields = ['document_name', 'note']
    list_editable = ['is_required', 'sort_order']
    ordering = ['sort_order', 'document_name']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('document_name', 'is_required')
        }),
        ('Qo\'shimcha', {
            'fields': ('document_file', 'note', 'sort_order')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_featured', 'sort_order', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['is_featured', 'is_active', 'sort_order']
    ordering = ['sort_order', 'question']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Sozlamalar', {
            'fields': ('is_featured', 'is_active', 'sort_order')
        }),
    )
