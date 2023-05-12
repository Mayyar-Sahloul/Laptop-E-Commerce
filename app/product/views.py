"""
Views for product API
"""

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.response import Response
from core.models import Product
from product import serializers
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma seperated list for tags to filter',
            ),
            OpenApiParameter(
                'brand',
                OpenApiTypes.STR,
                description='Comma seperated list for brands to filter',
            ),
            OpenApiParameter(
                'price',
                OpenApiTypes.INT,
                description='Maximum price to filter'
            ),
            OpenApiParameter(
                'color',
                OpenApiTypes.STR,
                description='color'
            )
        ]
    ),
    retrieve = extend_schema(
        parameters=[
            OpenApiParameter(
                'color',
                OpenApiTypes.STR,
                description='color'
            ),
        ]
    )
)

class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """View from manage product API"""

    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for the request"""
        if self.action=='list':
            return serializers.ProductSerializer
        return self.serializer_class

    def _get_params(self, qs):
        """return a list of the request parameters"""
        return [x for x in qs.split(',')]

    def get_queryset(self):
        """Filter products"""
        tags = self.request.query_params.get('tags')
        brand = self.request.query_params.get('brand')
        max_price = self.request.query_params.get('price')
        color = self.request.query_params.get('color')
        queryset = self.queryset

        if tags:
            tag_names = self._get_params(tags)
            queryset = queryset.filter(tags__name__in=tag_names)

        if brand:
            brand_names = self._get_params(brand)
            queryset = queryset.filter(brand__in=brand_names)

        if max_price:
            queryset = queryset.filter(price__lt=max_price)

        if color:
            color_names = self._get_params(color)
            queryset = queryset.filter(images__color__in=color_names)

        return queryset.distinct().order_by('-created_at')


    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific product and filter base on the color"""
        instance = self.get_object()
        color = self.request.query_params.get('color')
        serializer = self.get_serializer(instance)
        data = serializer.data

        if color:
            images = data['images']
            new_image = [im for im in images if im['color']==color]
            data['images'] = new_image

        return Response(data)
