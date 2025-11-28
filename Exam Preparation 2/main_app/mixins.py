from django.core.validators import MinLengthValidator
from django.db import models


class NationalityMixin(models.Model):
    nationality = models.CharField(max_length=50, default='Unknown')

    class Meta:
        abstract = True

class FullNameAndBirthDateMixin(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')

    class Meta:
        abstract = True


class IsAwardedAndLastUpdatedMixin(models.Model):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True