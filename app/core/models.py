"""
Data base models
"""

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.conf import settings
import uuid
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings


def image_file_path(instance, filename):
    """Generate file path for new recipe image """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    if type(instance).__name__ == 'User':
        return os.path.join('uploads', filename)

    else :
        return os.path.join('uploads', filename)

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user """
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return  superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to=image_file_path, blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Product(models.Model):
    """product object"""

    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=0, max_digits=5)
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    description = models.CharField(max_length=255, default='', blank=True)
    processor = models.CharField(max_length=255, default='', blank=True)
    memory = models.CharField(max_length=255, default='', blank=True)
    display = models.CharField(max_length=255, default='', blank=True)
    storage = models.CharField(max_length=255, default='', blank=True)
    os = models.CharField(max_length=255, default='', blank=True)
    is_laptop = models.BooleanField(default=False)
    brand = models.CharField(max_length=255, null=True)
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}({self.id})'


class ProductImage(models.Model):
    """Images for the product"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    color = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_file_path, blank=True, null=True)
    quantity = models.DecimalField(decimal_places=0, max_digits=5, default=1)

    def __str__(self):
        return f'{self.product.name}({self.product.id})-{self.color}'


class Tag(models.Model):
    """Tags for filtering products"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Cart for the user"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product_quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(decimal_places=3, max_digits=10, default=0, null=True)

    def __str__(self):
        return self.user.email


class CartProduct(models.Model):
    """Intermediate class to link number of the product
    in the cart with the product"""

    product = models.ForeignKey(
        'Product',
         on_delete=models.CASCADE,
    )

    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='cart_products'
    )
    quantity = models.PositiveIntegerField()
    color = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.product.name