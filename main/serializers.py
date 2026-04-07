from rest_framework import serializers
from .models import Statistic


class StatisticReadOnlySerializer(serializers.ModelSerializer):
    """GET so'rovlari uchun serializer - faqat o'qish uchun"""
    
    class Meta:
        model = Statistic
        fields = ['id', 'key', 'value', 'label', 'icon', 'sort_order', 'updated_at']
        read_only_fields = ['id', 'key', 'value', 'label', 'icon', 'sort_order', 'updated_at']


class StatisticWriteSerializer(serializers.ModelSerializer):
    """POST/PUT so'rovlari uchun serializer - yozish uchun"""
    
    class Meta:
        model = Statistic
        fields = ['key', 'value', 'label', 'icon', 'sort_order']
    
    def validate_key(self, value):
        """Kalitning noyobligini tekshirish"""
        if self.instance and self.instance.key != value:
            if Statistic.objects.filter(key=value).exists():
                raise serializers.ValidationError("Bu kalit allaqachon mavjud!")
        return value
    
    def validate_value(self, value):
        """Qiymat manfiy bo'lmasligi kerak"""
        if value < 0:
            raise serializers.ValidationError("Qiymat manfiy bo'lishi mumkin emas!")
        return value
