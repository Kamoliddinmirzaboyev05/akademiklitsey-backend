from rest_framework import serializers
from django.utils.text import slugify
from .models import News, Announcement, NewsImage, AnnouncementImage


class NewsImageSerializer(serializers.ModelSerializer):
    """Yangilik rasmlari uchun serializer"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsImage
        fields = ['id', 'image_url', 'caption', 'sort_order', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        """Rasm URL ni olish"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class NewsImageUploadSerializer(serializers.ModelSerializer):
    """Yangilik rasmlari yuklash uchun serializer"""
    
    class Meta:
        model = NewsImage
        fields = ['image', 'caption', 'sort_order']
    
    def create(self, validated_data):
        """Sort_order ni avtomatik belgilash"""
        if 'sort_order' not in validated_data:
            # Oxirgi sort_order ni olish va +1 qilish
            last_image = NewsImage.objects.filter(
                news=validated_data['news']
            ).order_by('-sort_order').first()
            
            if last_image:
                validated_data['sort_order'] = last_image.sort_order + 1
            else:
                validated_data['sort_order'] = 1
        
        return super().create(validated_data)


class NewsListSerializer(serializers.ModelSerializer):
    """Yangiliklar ro'yxati uchun serializer (qisqa ma'lumotlar)"""
    images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'short_description', 'thumbnail', 
            'views_count', 'published_at', 'images_count'
        ]
    
    def get_images_count(self, obj):
        """Yangilikdagi rasmlar soni"""
        return obj.images.count()


class NewsDetailSerializer(serializers.ModelSerializer):
    """Yangilik detallari uchun serializer (to'liq ma'lumotlar)"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    images = NewsImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'short_description', 'content', 'thumbnail',
            'views_count', 'status', 'is_featured', 'published_at', 
            'created_at', 'updated_at', 'created_by', 'created_by_name', 'images'
        ]
        read_only_fields = ['id', 'views_count', 'created_at', 'updated_at', 'created_by']


class NewsWriteSerializer(serializers.ModelSerializer):
    """Yangilik yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = News
        fields = [
            'title', 'short_description', 'content', 'thumbnail',
            'status', 'is_featured', 'published_at', 'slug'
        ]
    
    def validate_slug(self, value):
        """Slugning noyobligini tekshirish"""
        if self.instance and self.instance.slug != value:
            if News.objects.filter(slug=value).exists():
                raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        elif not self.instance and News.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        return value
    
    def create(self, validated_data):
        """Yangilik yaratishda slug va created_by ni avtomatik to'ldirish"""
        # Agar slug berilmagan bo'lsa, title dan avtomatik yaratish
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['title'])
        
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Yangilikni yangilash - slug bo'sh bo'lsa title dan yaratish"""
        if 'slug' in validated_data and (not validated_data['slug'] or validated_data['slug'].strip() == ''):
            validated_data['slug'] = slugify(validated_data.get('title', instance.title))
        
        return super().update(instance, validated_data)


class AnnouncementImageSerializer(serializers.ModelSerializer):
    """E'lon rasmlari uchun serializer"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnouncementImage
        fields = ['id', 'image_url', 'caption', 'sort_order', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        """Rasm URL ni olish"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AnnouncementImageUploadSerializer(serializers.ModelSerializer):
    """E'lon rasmlari yuklash uchun serializer"""
    
    class Meta:
        model = AnnouncementImage
        fields = ['image', 'caption', 'sort_order']
    
    def create(self, validated_data):
        """Sort_order ni avtomatik belgilash"""
        if 'sort_order' not in validated_data:
            # Oxirgi sort_order ni olish va +1 qilish
            last_image = AnnouncementImage.objects.filter(
                announcement=validated_data['announcement']
            ).order_by('-sort_order').first()
            
            if last_image:
                validated_data['sort_order'] = last_image.sort_order + 1
            else:
                validated_data['sort_order'] = 1
        
        return super().create(validated_data)


class AnnouncementListSerializer(serializers.ModelSerializer):
    """E'lonlar ro'yxati uchun serializer (qisqa ma'lumotlar)"""
    images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'slug', 'short_description', 'thumbnail',
            'views_count', 'is_important', 'expires_at', 'published_at', 'images_count'
        ]
    
    def get_images_count(self, obj):
        """E'londagi rasmlar soni"""
        return obj.images.count()


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    """E'lon detallari uchun serializer (to'liq ma'lumotlar)"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    images = AnnouncementImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'slug', 'short_description', 'content', 'thumbnail',
            'views_count', 'is_important', 'status', 'expires_at',
            'published_at', 'created_at', 'created_by', 'created_by_name', 'is_expired', 'images'
        ]
        read_only_fields = ['id', 'views_count', 'created_at', 'created_by']


class AnnouncementWriteSerializer(serializers.ModelSerializer):
    """E'lon yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = Announcement
        fields = [
            'title', 'short_description', 'content', 'thumbnail',
            'is_important', 'status', 'expires_at', 'published_at', 'slug'
        ]
    
    def validate_slug(self, value):
        """Slugning noyobligini tekshirish"""
        if self.instance and self.instance.slug != value:
            if Announcement.objects.filter(slug=value).exists():
                raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        elif not self.instance and Announcement.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        return value
    
    def create(self, validated_data):
        """E'lon yaratishda slug va created_by ni avtomatik to'ldirish"""
        # Agar slug berilmagan bo'lsa, title dan avtomatik yaratish
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['title'])
        
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """E'lonni yangilash - slug bo'sh bo'lsa title dan yaratish"""
        if 'slug' in validated_data and (not validated_data['slug'] or validated_data['slug'].strip() == ''):
            validated_data['slug'] = slugify(validated_data.get('title', instance.title))
        
        return super().update(instance, validated_data)
