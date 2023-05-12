"""
Serializers for the recipe API
"""

from rest_framework import serializers
from core.models import (
    Product,
    ProductImage,
    Tag
)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product photos"""

    class Meta:
        model = ProductImage
        fields = ['id', 'color', 'image']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products"""
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'rating', 'images',]
        read_only_fields = ['id']

class ProductDetailSerializer(ProductSerializer):
    """serializer for product details"""
    tags = TagSerializer(many=True)
    def __init__(self, instance, **kwargs):
        super().__init__(instance, **kwargs)

        if instance.is_laptop:
            self.Meta.fields = ProductSerializer.Meta.fields + [
                'description', 'processor', 'memory', 'display', 'storage', 'os', 'tags'
            ]
        else:
            self.Meta.fields = ProductSerializer.Meta.fields + ['description', 'tags']

    class Meta(ProductSerializer.Meta):
       pass


