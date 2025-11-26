from django.db import models
from django.core.exceptions import ValidationError



class StudentIDField(models.PositiveIntegerField):

    def to_python(self, value):
        try:
            return super().to_python(value)
        except ValidationError:
            raise ValueError("Invalid input for student ID")

    def get_prep_value(self, value):

        try:
            value = super().get_prep_value(value)
        except ValueError as e:
            raise e.__class__(
                "Invalid input for student ID"
            )

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return value

class MaskedCreditCardField(models.CharField):

    def to_python(self, value):
        card_length_validation = 16
        value = super().to_python(value)

        if value.startswith("****-****-****-"):
            return value

        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != card_length_validation:
            raise ValidationError("The card number must be exactly 16 characters long")

        return value

    def get_prep_value(self, value):
        last_numbers = value[-4:]

        if value.startswith("****-****-****-"):
            return value

        return f"****-****-****-{last_numbers}"
