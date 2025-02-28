"""
URl mappings for the product app
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from product import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]