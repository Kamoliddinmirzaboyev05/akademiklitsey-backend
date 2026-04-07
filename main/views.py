from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from accounts.permissions import IsAdminUser, IsAdminOrReadOnly
from .models import Statistic
from .serializers import StatisticReadOnlySerializer, StatisticWriteSerializer


class StatisticListCreateView(generics.GenericAPIView):
    """GET - barcha statistikalar, POST - yangi statistika yaratish (faqat admin)"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StatisticReadOnlySerializer
        return StatisticWriteSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]
    
    queryset = Statistic.objects.all()
    
    def get(self, request):
        """Barcha statistikalarni olish - hamma ko'rishi mumkin"""
        statistics = self.get_queryset()
        serializer = self.get_serializer(statistics, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Yangi statistika yaratish - faqat adminlar"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatisticDetailView(generics.GenericAPIView):
    """GET - bitta statistika, PUT/DELETE - faqat adminlar"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StatisticReadOnlySerializer
        return StatisticWriteSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]
    
    queryset = Statistic.objects.all()
    
    def get_object(self):
        """pk orqali statistikani olish"""
        return get_object_or_404(Statistic, pk=self.kwargs['pk'])
    
    def get(self, request, pk):
        """Bitta statistikani olish - hamma ko'rishi mumkin"""
        statistic = self.get_object()
        serializer = self.get_serializer(statistic)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Statistikani yangilash - faqat adminlar"""
        statistic = self.get_object()
        serializer = self.get_serializer(statistic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Statistikani o'chirish - faqat adminlar"""
        statistic = self.get_object()
        statistic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
