"""
Serializers for the Cart view API

"""


from rest_framework import serializers
from core.models import(
    ProductImage,
    Product,
    Cart,
    CartProduct,
)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for the image in the cart"""

    class Meta:
        model = ProductImage
        fields = ['image','color', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for  products in the cart"""
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images']
        read_only_fields = ['id']


class CartProductSerializer(serializers.ModelSerializer):
    """Serializer for the products in the cart"""
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'color']
        read_only_fields = ['id']



class CartSerializer(serializers.ModelSerializer):
    """Serilizer for the user Cart"""
    cart_products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_products', 'product_quantity', 'total_price']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """calculate the quantity and total price"""
        data = super().to_representation(instance)
        total_price = 0
        product_quantity = 0
        for cart_product in instance.cart_products.all():
            product = cart_product.product
            price = product.price
            quantity = cart_product.quantity
            total_price += price*quantity
            product_quantity += quantity

        data['total_price'] = total_price
        data['product_quantity'] = product_quantity
        return data

class AddCartSerializer(serializers.Serializer):
    """Serializer to use when adding products from the cart """
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    color = serializers.CharField()

    def validate(self, data):
        """check if the quantity and color are valid"""
        product = Product.objects.get(id=data['id'])
        product_image = product.images.get(color=data['color'])
        if product_image.quantity<data['quantity']:
            msg = f'There is only {product.quantity} available of this color'
            raise serializers.ValidationError({
                'quantity': [msg]
            })

        return data

class DeleteCartSerializer(serializers.Serializer):
    """Serializer for removing products from the cart"""
    id = serializers.IntegerField()
