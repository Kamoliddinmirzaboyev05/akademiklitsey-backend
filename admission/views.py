from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from accounts.permissions import IsAdminUser
from .models import AdmissionInfo, AdmissionSubject, AdmissionDocument, FAQ
from .serializers import (
    AdmissionInfoSerializer, AdmissionCurrentSerializer, AdmissionInfoWriteSerializer,
    AdmissionSubjectSerializer, AdmissionSubjectWriteSerializer,
    AdmissionDocumentSerializer, AdmissionDocumentWriteSerializer,
    FAQSerializer, FAQWriteSerializer
)


class BaseAdmissionView(generics.GenericAPIView):
    """Admission uchun asosiy view - umumiy funksiyalar"""
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]


class AdmissionCurrentView(BaseAdmissionView):
    """Joriy yil qabul ma'lumotlari - GET, PUT"""
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdmissionCurrentSerializer
        return AdmissionInfoWriteSerializer
    
    def get_object(self):
        """Joriy yil qabul ma'lumotlarini olish"""
        try:
            return AdmissionInfo.objects.filter(is_active=True).first()
        except AdmissionInfo.DoesNotExist:
            return None
    
    def get(self, request):
        """Joriy yil qabul ma'lumotlari (barcha ma'lumotlar bilan)"""
        admission_info = self.get_object()
        if not admission_info:
            return Response({
                'success': False,
                'message': 'Joriy yil qabul ma\'lumotlari topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)
            
        subjects = AdmissionSubject.objects.all().order_by('sort_order', 'subject_name')
        documents = AdmissionDocument.objects.all().order_by('sort_order', 'document_name')
        
        data = {
            'success': True,
            'data': {
                'admission_info': AdmissionInfoSerializer(admission_info).data,
                'subjects': AdmissionSubjectSerializer(subjects, many=True).data,
                'documents': AdmissionDocumentSerializer(documents, many=True).data
            }
        }
        return Response(data)
    
    def put(self, request):
        """Joriy yil qabul ma'lumotlarini yangilash - faqat admin"""
        admission_info = self.get_object()
        if not admission_info:
            return Response({
                'success': False,
                'message': 'Joriy yil qabul ma\'lumotlari topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = self.get_serializer(admission_info, data=request.data)
        if serializer.is_valid():
            updated_info = serializer.save()
            response_serializer = AdmissionCurrentSerializer(updated_info)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdmissionHistoryView(generics.GenericAPIView):  # yoki BaseAdmissionView dan meros olsangiz ham bo'ladi
    """O'tgan yillar tarixi - GET"""

    permission_classes = []  # agar kerak bo'lsa
    queryset = AdmissionInfo.objects.all()

    # Swagger uchun serializer_class ni belgilaymiz (xatolik chiqmasligi uchun)
    serializer_class = AdmissionInfoSerializer

    @swagger_auto_schema(auto_schema=None)  # Bu view Swaggerda ko'rinmasin
    def get(self, request):
        """O'tgan yillar qabul tarixi"""
        admissions = AdmissionInfo.objects.filter(
            is_active=False
        ).order_by('-academic_year')

        serializer = AdmissionInfoSerializer(admissions, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

class AdmissionSubjectsView(BaseAdmissionView):
    """Imtihon fanlari - GET, POST"""
    
    model = AdmissionSubject
    queryset = AdmissionSubject.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdmissionSubjectSerializer
        return AdmissionSubjectWriteSerializer
    
    def get(self, request):
        """Imtihon fanlari ro'yxati"""
        subjects = AdmissionSubject.objects.all().order_by('sort_order', 'subject_name')
        serializer = self.get_serializer(subjects, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        """Yangi imtihon fani qo'shish - faqat admin"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            response_serializer = AdmissionSubjectSerializer(subject)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdmissionSubjectDetailView(BaseAdmissionView):
    """Bitta imtihon fani - GET, PUT, DELETE"""
    
    model = AdmissionSubject
    queryset = AdmissionSubject.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdmissionSubjectSerializer
        return AdmissionSubjectWriteSerializer
    
    def get_object(self):
        return get_object_or_404(AdmissionSubject, pk=self.kwargs['pk'])
    
    def get(self, request, pk):
        """Bitta imtihon fani ma'lumotlari"""
        subject = self.get_object()
        serializer = self.get_serializer(subject)
        return Response({'success': True, 'data': serializer.data})
    
    def put(self, request, pk):
        """Imtihon fanini yangilash - faqat admin"""
        subject = self.get_object()
        serializer = self.get_serializer(subject, data=request.data)
        if serializer.is_valid():
            updated_subject = serializer.save()
            response_serializer = AdmissionSubjectSerializer(updated_subject)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Imtihon fanini o'chirish - faqat admin"""
        subject = self.get_object()
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdmissionDocumentsView(BaseAdmissionView):
    """Talab qilinadigan hujjatlar - GET, POST"""
    
    model = AdmissionDocument
    queryset = AdmissionDocument.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdmissionDocumentSerializer
        return AdmissionDocumentWriteSerializer
    
    def get(self, request):
        """Talab qilinadigan hujjatlar ro'yxati"""
        documents = self.get_queryset().order_by('sort_order', 'document_name')
        serializer = self.get_serializer(documents, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        """Yangi hujjat qo'shish - faqat admin"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            response_serializer = AdmissionDocumentSerializer(document)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdmissionDocumentDetailView(BaseAdmissionView):
    """Bitta hujjat - GET, PUT, DELETE"""
    
    model = AdmissionDocument
    queryset = AdmissionDocument.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdmissionDocumentSerializer
        return AdmissionDocumentWriteSerializer
    
    def get_object(self):
        return get_object_or_404(AdmissionDocument, pk=self.kwargs['pk'])
    
    def get(self, request, pk):
        """Bitta hujjat ma'lumotlari"""
        document = self.get_object()
        serializer = self.get_serializer(document)
        return Response({'success': True, 'data': serializer.data})
    
    def put(self, request, pk):
        """Hujjatni yangilash - faqat admin"""
        document = self.get_object()
        serializer = self.get_serializer(document, data=request.data)
        if serializer.is_valid():
            updated_document = serializer.save()
            response_serializer = AdmissionDocumentSerializer(updated_document)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Hujjatni o'chirish - faqat admin"""
        document = self.get_object()
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FAQListView(BaseAdmissionView):
    """FAQ lar ro'yxati - GET, POST"""
    
    model = FAQ
    queryset = FAQ.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FAQSerializer
        return FAQWriteSerializer
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        
        # Kategoriya bo'yicha filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('sort_order', 'question')
    
    def get(self, request):
        """Barcha FAQ lar"""
        faqs = self.get_queryset()
        serializer = self.get_serializer(faqs, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        """Yangi FAQ qo'shish - faqat admin"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            faq = serializer.save()
            response_serializer = FAQSerializer(faq)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FAQFeaturedView(BaseAdmissionView):
    """Bosh sahifa uchun FAQ lar - GET"""
    
    model = FAQ
    queryset = FAQ.objects.all()
    
    def get_serializer_class(self):
        return FAQSerializer
    
    def get(self, request):
        """Bosh sahifaga chiqariladigan FAQ lar"""
        faqs = FAQ.objects.filter(is_featured=True, is_active=True).order_by('sort_order', 'question')
        serializer = self.get_serializer(faqs, many=True)
        return Response({'success': True, 'data': serializer.data})


class FAQDetailView(BaseAdmissionView):
    """Bitta FAQ - GET, PUT, DELETE"""
    
    model = FAQ
    queryset = FAQ.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FAQSerializer
        return FAQWriteSerializer
    
    def get_object(self):
        return get_object_or_404(FAQ, pk=self.kwargs['pk'])
    
    def get(self, request, pk):
        """Bitta FAQ ma'lumotlari"""
        faq = self.get_object()
        serializer = self.get_serializer(faq)
        return Response({'success': True, 'data': serializer.data})
    
    def put(self, request, pk):
        """FAQ ni yangilash - faqat admin"""
        faq = self.get_object()
        serializer = self.get_serializer(faq, data=request.data)
        if serializer.is_valid():
            updated_faq = serializer.save()
            response_serializer = FAQSerializer(updated_faq)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """FAQ ni o'chirish - faqat admin"""
        faq = self.get_object()
        faq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
