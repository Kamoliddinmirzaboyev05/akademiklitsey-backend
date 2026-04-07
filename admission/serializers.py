from rest_framework import serializers
from .models import AdmissionInfo, AdmissionSubject, AdmissionDocument, FAQ


class AdmissionInfoSerializer(serializers.ModelSerializer):
    """Qabul ma'lumotlari uchun serializer"""
    
    class Meta:
        model = AdmissionInfo
        fields = [
            'id', 'academic_year', 'total_quota', 'grant_quota', 'contract_quota',
            'contract_price', 'application_start', 'application_end', 'exam_date',
            'results_date', 'online_apply_url', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdmissionSubjectSerializer(serializers.ModelSerializer):
    """Imtihon fanlari uchun serializer"""
    subject_type_display = serializers.CharField(source='get_subject_type_display', read_only=True)
    
    class Meta:
        model = AdmissionSubject
        fields = ['id', 'subject_name', 'subject_type', 'subject_type_display', 'max_score', 'description', 'sort_order']
        read_only_fields = ['id']


class AdmissionDocumentSerializer(serializers.ModelSerializer):
    """Talab qilinadigan hujjatlar uchun serializer"""
    document_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AdmissionDocument
        fields = ['id', 'document_name', 'document_file', 'document_file_url', 'is_required', 'note', 'sort_order']
        read_only_fields = ['id', 'document_file_url']
    
    def get_document_file_url(self, obj):
        """Fayl URL ni olish"""
        if obj.document_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.document_file.url)
            return obj.document_file.url
        return None


class FAQSerializer(serializers.ModelSerializer):
    """FAQ uchun serializer"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'category_display', 'is_featured', 'sort_order', 'is_active']
        read_only_fields = ['id']


class AdmissionCurrentSerializer(serializers.Serializer):
    """Joriy yil qabul ma'lumotlari uchun kompleks serializer"""
    admission_info = AdmissionInfoSerializer()
    subjects = AdmissionSubjectSerializer(many=True)
    documents = AdmissionDocumentSerializer(many=True)


class AdmissionInfoWriteSerializer(serializers.ModelSerializer):
    """Qabul ma'lumotlarini yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = AdmissionInfo
        fields = [
            'academic_year', 'total_quota', 'grant_quota', 'contract_quota',
            'contract_price', 'application_start', 'application_end', 'exam_date',
            'results_date', 'online_apply_url', 'is_active'
        ]
    
    def validate(self, data):
        """Kvotalar va sanalar tekshiruvi"""
        total_quota = data.get('total_quota')
        grant_quota = data.get('grant_quota')
        contract_quota = data.get('contract_quota')
        
        # Kvotalar tekshiruvi
        if total_quota and grant_quota and contract_quota:
            if grant_quota + contract_quota > total_quota:
                raise serializers.ValidationError({
                    'quota_error': 'Grant va kontrakt kvotalari yig\'indisi jami kvotadan oshmasligi kerak'
                })
        
        # Sanalar tekshiruvi
        application_start = data.get('application_start')
        application_end = data.get('application_end')
        exam_date = data.get('exam_date')
        results_date = data.get('results_date')
        
        if application_start and application_end and application_start > application_end:
            raise serializers.ValidationError({
                'date_error': 'Ariza qabul boshlanishi sanasi tugash sanasidan oldin bo\'lishi kerak'
            })
        
        if exam_date and application_end and exam_date < application_end:
            raise serializers.ValidationError({
                'date_error': 'Imtihon sanasi ariza qabul tugash sanasidan keyin bo\'lishi kerak'
            })
        
        if results_date and exam_date and results_date < exam_date:
            raise serializers.ValidationError({
                'date_error': 'Natijalar e\'lon qilish sanasi imtihon sanasidan keyin bo\'lishi kerak'
            })
        
        return data


class AdmissionSubjectWriteSerializer(serializers.ModelSerializer):
    """Imtihon fanlarini yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = AdmissionSubject
        fields = ['subject_name', 'subject_type', 'max_score', 'description', 'sort_order']


class AdmissionDocumentWriteSerializer(serializers.ModelSerializer):
    """Hujjatlarni yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = AdmissionDocument
        fields = ['document_name', 'document_file', 'is_required', 'note', 'sort_order']


class FAQWriteSerializer(serializers.ModelSerializer):
    """FAQ larni yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'is_featured', 'sort_order', 'is_active']
