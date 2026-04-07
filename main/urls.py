from django.urls import path
from .views import StatisticListCreateView, StatisticDetailView

app_name = 'main'

urlpatterns = [
    path('statistics/', StatisticListCreateView.as_view(), name='statistic-list-create'),
    path('statistics/<int:pk>/', StatisticDetailView.as_view(), name='statistic-detail'),
]
