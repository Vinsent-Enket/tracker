from django.urls import path

from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import index, AddictionViewSet

app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r'addict', AddictionViewSet, basename='adict')

urlpatterns = [path('', index, name='index'),
               ] + router.urls
