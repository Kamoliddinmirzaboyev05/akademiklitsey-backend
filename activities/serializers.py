from rest_framework import serializers
from .models import Circle


class CircleListSerializer(serializers.ModelSerializer):
    """To'garaklar ro'yxati uchun serializer"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    available_slots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Circle
        fields = [
            'id', 'name', 'slug', 'category', 'category_display',
            'teacher', 'teacher_name', 'max_students', 'current_students',
            'available_slots', 'is_full', 'schedule', 'room', 'photo', 'photo_url',
            'is_active', 'sort_order'
        ]
    
    def get_photo_url(self, obj):
        """Rasm URL ni olish"""
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class CircleDetailSerializer(CircleListSerializer):
    """To'garak detallari uchun serializer"""
    
    class Meta(CircleListSerializer.Meta):
        fields = CircleListSerializer.Meta.fields


class CircleWriteSerializer(serializers.ModelSerializer):
    """To'garak yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = Circle
        fields = [
            'name', 'slug', 'category', 'description', 'teacher',
            'max_students', 'current_students', 'schedule', 'room',
            'photo', 'is_active', 'sort_order'
        ]
    
    def validate_slug(self, value):
        """Slugning noyobligini tekshirish"""
        if self.instance and self.instance.slug != value:
            if Circle.objects.filter(slug=value).exists():
                raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        elif not self.instance and Circle.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        return value
    
    def validate_current_students(self, value):
        """Hozirgi o'quvchilar soni maksimaldan oshmasligi kerak"""
        max_students = self.initial_data.get('max_students')
        if max_students and value > int(max_students):
            raise serializers.ValidationError("Hozirgi o'quvchilar soni maksimal o'rinlar sonidan oshmasligi kerak!")
        return value
    
    def create(self, validated_data):
        """To'garak yaratishda slug avtomatik yaratish"""
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = validated_data['name'].lower().replace(' ', '-')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """To'garakni yangilash - slug bo'sh bo'lsa name dan yaratish"""
        if 'slug' in validated_data and (not validated_data['slug'] or validated_data['slug'].strip() == ''):
            validated_data['slug'] = validated_data.get('name', instance.name).lower().replace(' ', '-')
        
        # Hozirgi o'quvchilar sonini tekshirish
        if 'current_students' in validated_data and 'max_students' in validated_data:
            if validated_data['current_students'] > validated_data['max_students']:
                raise serializers.ValidationError("Hozirgi o'quvchilar soni maksimal o'rinlar sonidan oshmasligi kerak!")
        elif 'current_students' in validated_data and instance.max_students:
            if validated_data['current_students'] > instance.max_students:
                raise serializers.ValidationError("Hozirgi o'quvchilar soni maksimal o'rinlar sonidan oshmasligi kerak!")
        
        return super().update(instance, validated_data)
