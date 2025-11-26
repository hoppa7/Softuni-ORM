from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator
from django.db import models
from .validators import *
from .mixin import *

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, validators=[validate_name])
    age = models.PositiveIntegerField(validators=[check_age])
    email = models.EmailField(error_messages={'invalid': "Enter a valid email address"})
    phone_number = models.CharField(max_length=13,
                                    validators=[
                                        RegexValidator(
                                        regex=r'^\+359\d{9}$', message="Phone number must start with '+359' followed by 9 digits")])
    website_url = models.URLField(error_messages={'invalid': "Enter a valid URL"})


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

class Book(BaseMedia):
    AUTHOR_MIN_LENGTH_VALUE = 5
    ISBN_MIN_LENGTH_VALUE = 6

    author = models.CharField(max_length=100, validators=[MinLengthValidator(
        limit_value=AUTHOR_MIN_LENGTH_VALUE, message="Author must be at least 5 characters long"
    )])
    isb = models.CharField(max_length=20, validators=[MinLengthValidator(
        limit_value=ISBN_MIN_LENGTH_VALUE, message="ISBN must be at least 6 characters long"
    )])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'

class Movie(BaseMedia):
    DIRECTOR_MIN_LENGTH_VALUE = 8
    director = models.CharField(max_length=100, validators=[MinLengthValidator(
        limit_value=DIRECTOR_MIN_LENGTH_VALUE, message="Director must be at least 8 characters long"
    )])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'

class Music(BaseMedia):
    ARTIST_MIN_LENGTH_VALUE = 9
    artist = models.CharField(max_length=100, validators=[MinLengthValidator(
        limit_value=ARTIST_MIN_LENGTH_VALUE, message="Artist must be at least 9 characters long"
    )])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'


class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2.00')
    PRODUCT_NAME: str = 'Product'

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return self.price * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal):
        return weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self):
        return f"{self.PRODUCT_NAME}: {self.name}"

class DiscountedProduct(Product):
    DISCOUNT_PERCENT: Decimal = Decimal('0.20')
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.50')
    PRODUCT_NAME: str = 'Discounted Product'
    PRICE_WITHOUT_DISCOUNT: Decimal = Decimal('0.20')

    def calculate_price_without_discount(self):
        return self.price * (1 + self.PRICE_WITHOUT_DISCOUNT)

    class Meta:
        proxy = True


class Hero(models.Model, RechargeEnergyMixin):
    ABILITY_ENERGY_CONSUMPTION: int = 0

    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    @property
    def required_energy_message(self):
        return ''

    @property
    def successful_ability_usage_message(self):
        return ''

    def use_ability(self):
        if self.energy < self.ABILITY_ENERGY_CONSUMPTION:
            return self.required_energy_message

        self.energy = max(self.energy - self.ABILITY_ENERGY_CONSUMPTION, 1)
        return self.successful_ability_usage_message



class SpiderHero(Hero):

    def swing_from_buildings(self):
        self.use_ability()

    @property
    def required_energy_message(self):
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_usage_message(self):
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True

class FlashHero(Hero):

    def run_at_super_speed(self):
        self.use_ability()

    @property
    def required_energy_message(self):
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_usage_message(self):
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['search_vector'])
        ]