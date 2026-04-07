from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from accounts.permissions import IsAdminUser
from content.pagination import CustomPagination
from .models import Circle
from .serializers import CircleListSerializer, CircleDetailSerializer, CircleWriteSerializer


class BaseCircleView(generics.GenericAPIView):
    """Circle uchun asosiy view - umumiy funksiyalar"""
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Faqat active to'garaklarni ko'rsatish (GET so'rovlari uchun)
        if self.request.method == 'GET':
            queryset = queryset.filter(is_active=True)
        
        # Search funksiyasi
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset


class CircleListView(BaseCircleView):
    """To'garaklar ro'yxati - GET, POST"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CircleListSerializer
        return CircleWriteSerializer
    
    queryset = Circle.objects.all()
    filterset_fields = ['category', 'is_active']
    
    def get(self, request):
        """To'garaklar ro'yxati - pagination bilan"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        """Yangi to'garak qo'shish - faqat admin"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            circle = serializer.save()
            response_serializer = CircleDetailSerializer(circle)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CircleDetailView(BaseCircleView):
    """Bitta to'garak - GET, PUT, DELETE"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CircleDetailSerializer
        return CircleWriteSerializer
    
    queryset = Circle.objects.all()
    
    def get_object(self):
        return get_object_or_404(Circle, slug=self.kwargs['slug'])
    
    def get(self, request, slug):
        """Bitta to'garakni ko'rish"""
        circle = self.get_object()
        # Faqat active to'garakni ko'rish mumkin
        if not circle.is_active:
            return Response(
                {'error': 'Bu to\'garak faol emas'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(circle)
        return Response({'success': True, 'data': serializer.data})
    
    def put(self, request, slug):
        """To'garakni yangilash - faqat admin"""
        circle = self.get_object()
        serializer = self.get_serializer(circle, data=request.data)
        if serializer.is_valid():
            updated_circle = serializer.save()
            response_serializer = CircleDetailSerializer(updated_circle)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug):
        """To'garakni o'chirish - faqat admin"""
        circle = self.get_object()
        circle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
