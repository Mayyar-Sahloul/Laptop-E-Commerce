"""
Views for the cart API
"""

from core.models import(
    Cart,
    Product,
    CartProduct,
)
from cart import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class CartViewSet(viewsets.ViewSet):
    """View for manage cart API"""

    serializer_class = serializers.CartSerializer
    queryset = Cart.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return serializer class for the request"""
        if self.action=='add_product':
            return serializers.AddCartSerializer

        elif self.action=='remove_product':
            return serializers.DeleteCartSerializer
        return self.serializer_class


    def list(self, request):
        """Retrieve the current user cart"""
        queryset = Cart.objects.get(user=request.user)
        serializer = serializers.CartSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def add_product(self, request, pk=None):
        """ Add product to user cart"""

        cart = Cart.objects.get(user=request.user)
        serializer = serializers.AddCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data.get('id')
            quantity = request.data.get('quantity')
            product = Product.objects.get(id=product_id)
            cart_product = CartProduct.objects.create(product=product, quantity=quantity, cart=cart)
            serializer = serializers.CartProductSerializer(cart_product)
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def remove_product(self, request, pk=None):
        """ remove product from user cart"""

        id = request.data.get('id')
        cart_product = CartProduct.objects.get(id=id)
        serializer = serializers.CartProductSerializer(cart_product)
        cart_product.delete()
        return Response(serializer.data)






