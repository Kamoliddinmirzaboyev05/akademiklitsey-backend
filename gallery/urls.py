from django.urls import path
from .views import (
    GalleryAlbumListView, GalleryAlbumDetailView, GalleryPhotoUploadView, GalleryPhotoDeleteView,
    UsefulLinkListView, UsefulLinkDetailView
)

app_name = 'gallery'

urlpatterns = [
    # Gallery endpoints
    path('gallery/albums/', GalleryAlbumListView.as_view(), name='gallery-album-list'),
    path('gallery/albums/<slug:slug>/', GalleryAlbumDetailView.as_view(), name='gallery-album-detail'),
    path('gallery/albums/<slug:slug>/photos/', GalleryPhotoUploadView.as_view(), name='gallery-photo-upload'),
    path('gallery/photos/<int:pk>/', GalleryPhotoDeleteView.as_view(), name='gallery-photo-delete'),
    
    # Useful Links endpoints
    path('useful-links/', UsefulLinkListView.as_view(), name='useful-link-list'),
    path('useful-links/<int:pk>/', UsefulLinkDetailView.as_view(), name='useful-link-detail'),
]
