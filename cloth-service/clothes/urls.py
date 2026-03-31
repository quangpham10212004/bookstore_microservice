from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClothViewSet

router = DefaultRouter()
router.register(r"clothes", ClothViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
