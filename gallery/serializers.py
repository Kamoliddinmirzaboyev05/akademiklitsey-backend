from rest_framework import serializers
from .models import GalleryAlbum, GalleryPhoto, UsefulLink


class GalleryPhotoSerializer(serializers.ModelSerializer):
    """Galereya rasmlari uchun serializer"""
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryPhoto
        fields = ['id', 'image_url', 'thumbnail_url', 'caption', 'sort_order', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        """Asosiy rasm URL ni olish"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_thumbnail_url(self, obj):
        """Kichik rasm URL ni olish"""
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None


class GalleryAlbumListSerializer(serializers.ModelSerializer):
    """Galereya albomlari ro'yxati uchun serializer"""
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryAlbum
        fields = [
            'id', 'title', 'slug', 'description', 'cover_image', 'cover_image_url',
            'event_date', 'photos_count', 'is_active', 'sort_order', 'created_at'
        ]
        read_only_fields = ['id', 'photos_count', 'created_at']
    
    def get_cover_image_url(self, obj):
        """Muqova rasm URL ni olish"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class GalleryAlbumDetailSerializer(GalleryAlbumListSerializer):
    """Galereya albomi detallari uchun serializer"""
    photos = GalleryPhotoSerializer(many=True, read_only=True)
    
    class Meta(GalleryAlbumListSerializer.Meta):
        fields = GalleryAlbumListSerializer.Meta.fields + ['photos', 'updated_at']


class GalleryAlbumWriteSerializer(serializers.ModelSerializer):
    """Galereya albomlarini yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = GalleryAlbum
        fields = [
            'title', 'slug', 'description', 'cover_image', 'event_date',
            'is_active', 'sort_order'
        ]
    
    def validate_slug(self, value):
        """Slugning noyobligini tekshirish"""
        if self.instance and self.instance.slug != value:
            if GalleryAlbum.objects.filter(slug=value).exists():
                raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        elif not self.instance and GalleryAlbum.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Bu slug allaqachon mavjud!")
        return value
    
    def create(self, validated_data):
        """Album yaratishda slug avtomatik yaratish"""
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = validated_data['title'].lower().replace(' ', '-')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Albumni yangilash - slug bo'sh bo'lsa title dan yaratish"""
        if 'slug' in validated_data and (not validated_data['slug'] or validated_data['slug'].strip() == ''):
            validated_data['slug'] = validated_data.get('title', instance.title).lower().replace(' ', '-')
        
        return super().update(instance, validated_data)


class GalleryPhotoUploadSerializer(serializers.ModelSerializer):
    """Galereya rasmlarini yuklash uchun serializer"""
    
    class Meta:
        model = GalleryPhoto
        fields = ['image', 'thumbnail', 'caption', 'sort_order']
    
    def validate(self, data):
        """Rasm yuklash tekshiruvi"""
        if not data.get('image'):
            raise serializers.ValidationError("Asosiy rasm yuklash shart!")
        return data


class UsefulLinkSerializer(serializers.ModelSerializer):
    """Foydali havolalar uchun serializer"""
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UsefulLink
        fields = ['id', 'name', 'url', 'logo', 'logo_url', 'description', 'sort_order', 'is_active']
        read_only_fields = ['id']
    
    def get_logo_url(self, obj):
        """Logo URL ni olish"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class UsefulLinkWriteSerializer(serializers.ModelSerializer):
    """Foydali havolalarni yaratish/tahrirlash uchun serializer"""
    
    class Meta:
        model = UsefulLink
        fields = ['name', 'url', 'logo', 'description', 'sort_order', 'is_active']
