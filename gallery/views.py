from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from accounts.permissions import IsAdminUser
from content.pagination import CustomPagination
from .models import GalleryAlbum, GalleryPhoto, UsefulLink
from .serializers import (
    GalleryAlbumListSerializer, GalleryAlbumDetailSerializer, GalleryAlbumWriteSerializer,
    GalleryPhotoSerializer, GalleryPhotoUploadSerializer,
    UsefulLinkSerializer, UsefulLinkWriteSerializer
)


class BaseGalleryView(generics.GenericAPIView):
    """Gallery uchun asosiy view - umumiy funksiyalar"""
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Faqat active albomlarni ko'rsatish (GET so'rovlari uchun)
        if self.request.method == 'GET':
            if hasattr(self, 'model') and self.model == GalleryAlbum:
                queryset = queryset.filter(is_active=True)
            elif hasattr(self, 'model') and self.model == UsefulLink:
                queryset = queryset.filter(is_active=True)
        
        # Search funksiyasi
        search = self.request.query_params.get('search', None)
        if search:
            if hasattr(self, 'model') and self.model == GalleryAlbum:
                queryset = queryset.filter(
                    Q(title__icontains=search) | 
                    Q(description__icontains=search)
                )
            elif hasattr(self, 'model') and self.model == UsefulLink:
                queryset = queryset.filter(
                    Q(name__icontains=search) | 
                    Q(description__icontains=search)
                )
        
        return queryset


class GalleryAlbumListView(BaseGalleryView):
    """Galereya albomlari ro'yxati - GET, POST"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GalleryAlbumListSerializer
        return GalleryAlbumWriteSerializer
    
    model = GalleryAlbum
    queryset = GalleryAlbum.objects.all()
    filterset_fields = ['is_active', 'event_date']
    
    def get(self, request):
        """Albomlar ro'yxati - pagination bilan"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        """Yangi albom qo'shish - faqat admin"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            album = serializer.save()
            response_serializer = GalleryAlbumDetailSerializer(album)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryAlbumDetailView(BaseGalleryView):
    """Bitta albom - GET, PUT, DELETE"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GalleryAlbumDetailSerializer
        return GalleryAlbumWriteSerializer
    
    model = GalleryAlbum
    queryset = GalleryAlbum.objects.all()
    
    def get_object(self):
        return get_object_or_404(GalleryAlbum, slug=self.kwargs['slug'])
    
    def get(self, request, slug):
        """Bitta albomni ko'rish (fotolar bilan)"""
        album = self.get_object()
        # Faqat active albomni ko'rish mumkin
        if not album.is_active:
            return Response(
                {'error': 'Bu albom faol emas'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(album)
        return Response({'success': True, 'data': serializer.data})
    
    def put(self, request, slug):
        """Albomni yangilash - faqat admin"""
        album = self.get_object()
        serializer = self.get_serializer(album, data=request.data)
        if serializer.is_valid():
            updated_album = serializer.save()
            response_serializer = GalleryAlbumDetailSerializer(updated_album)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug):
        """Albomni o'chirish - faqat admin"""
        album = self.get_object()
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GalleryPhotoUploadView(BaseGalleryView):
    """Albomga rasm yuklash - faqat adminlar"""
    
    def get_serializer_class(self):
        return GalleryPhotoUploadSerializer
    
    def get_object(self):
        return get_object_or_404(GalleryAlbum, slug=self.kwargs['slug'])
    
    def post(self, request, slug):
        """Albomga yangi rasm yuklash"""
        album = self.get_object()
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Sort_order ni avtomatik belgilash
            if 'sort_order' not in serializer.validated_data:
                last_photo = GalleryPhoto.objects.filter(album=album).order_by('-sort_order').first()
                if last_photo:
                    serializer.validated_data['sort_order'] = last_photo.sort_order + 1
                else:
                    serializer.validated_data['sort_order'] = 1
            
            serializer.save(album=album)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryPhotoDeleteView(BaseGalleryView):
    """Rasmni o'chirish - faqat adminlar"""
    
    model = GalleryPhoto
    queryset = GalleryPhoto.objects.all()
    
    def get_object(self):
        return get_object_or_404(GalleryPhoto, pk=self.kwargs['pk'])
    
    def delete(self, request, pk):
        """Rasmani o'chirish - faqat admin"""
        photo = self.get_object()
        album = photo.album
        
        # Albomning photos_count ni yangilash
        album.photos_count = album.photos.count() - 1
        album.save()
        
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsefulLinkListView(BaseGalleryView):
    """Foydali havolalar ro'yxati - GET, POST"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsefulLinkSerializer
        return UsefulLinkWriteSerializer
    
    model = UsefulLink
    queryset = UsefulLink.objects.all()
    filterset_fields = ['is_active']
    
    def get(self, request):
        """Barcha havolalar"""
        links = self.get_queryset()
        serializer = self.get_serializer(links, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        """Yangi havola qo'shish - faqat admin"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            link = serializer.save()
            response_serializer = UsefulLinkSerializer(link)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsefulLinkDetailView(BaseGalleryView):
    """Bitta havola - GET, PUT, DELETE"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsefulLinkSerializer
        return UsefulLinkWriteSerializer
    
    model = UsefulLink
    queryset = UsefulLink.objects.all()
    
    def get_object(self):
        return get_object_or_404(UsefulLink, pk=self.kwargs['pk'])
    
    def get(self, request, pk):
        """Bitta havolani ko'rish"""
        link = self.get_object()
        # Faqat active havolani ko'rish mumkin
        if not link.is_active:
            return Response(
                {'error': 'Bu havola faol emas'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(link)
        return Response({'success': True, 'data': serializer.data})
    
    def put(self, request, pk):
        """Havolani yangilash - faqat admin"""
        link = self.get_object()
        serializer = self.get_serializer(link, data=request.data)
        if serializer.is_valid():
            updated_link = serializer.save()
            response_serializer = UsefulLinkSerializer(updated_link)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Havolani o'chirish - faqat admin"""
        link = self.get_object()
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
