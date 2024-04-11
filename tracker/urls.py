from django.urls import path

from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import index, AddictionViewSet, PeriodicityUpdateAPIView

app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r'addict', AddictionViewSet, basename='addict')

urlpatterns = [path('', index, name='index'),
               path('periodicity/', PeriodicityUpdateAPIView.as_view(), name='periodicity'),
               ] + router.urls
