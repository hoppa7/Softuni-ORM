from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator, URLValidator


def validate_name(value):
    if not value.isalpha():
        raise ValidationError("Name can only contain letters and spaces")

def check_age(value):
    if value < 18:
        raise ValidationError("Age must be greater than or equal to 18")

