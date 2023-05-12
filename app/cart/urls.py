"""
URl mappings for the cart app
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from cart import views


router = DefaultRouter()
router.register('cart', views.CartViewSet)

urlpatterns = [
    path('', include(router.urls))
]