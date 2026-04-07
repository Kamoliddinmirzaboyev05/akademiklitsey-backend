from django.urls import path
from .views import (
    NewsListView, NewsFeaturedView, NewsDetailView, NewsIncrementViewsView, NewsImageView, NewsImageUploadView,
    AnnouncementListView, AnnouncementFeaturedView, AnnouncementDetailView, AnnouncementImageView, AnnouncementImageUploadView
)

app_name = 'content'

urlpatterns = [
    # News endpoints
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/featured/', NewsFeaturedView.as_view(), name='news-featured'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/<slug:slug>/views/', NewsIncrementViewsView.as_view(), name='news-increment-views'),
    path('news/<slug:slug>/images/', NewsImageUploadView.as_view(), name='news-image-upload'),
    path('news/<slug:slug>/images/<int:pk>/', NewsImageView.as_view(), name='news-image-delete'),
    
    # Announcement endpoints
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/featured/', AnnouncementFeaturedView.as_view(), name='announcement-featured'),
    path('announcements/<slug:slug>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcements/<slug:slug>/images/', AnnouncementImageUploadView.as_view(), name='announcement-image-upload'),
    path('announcements/<slug:slug>/images/<int:pk>/', AnnouncementImageView.as_view(), name='announcement-image-delete'),
]
