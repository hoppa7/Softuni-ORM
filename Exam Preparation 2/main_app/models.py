from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from .mixins import NationalityMixin, IsAwardedAndLastUpdatedMixin, FullNameAndBirthDateMixin
from .choices import GenreChoices
from .managers import DirectorManager

# Create your models here.
class Director(NationalityMixin, FullNameAndBirthDateMixin):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )

    objects = DirectorManager()

class Actor(NationalityMixin, FullNameAndBirthDateMixin, IsAwardedAndLastUpdatedMixin):
    pass

class Movie(IsAwardedAndLastUpdatedMixin):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        default=0.0
    )
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey("Director", on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey("Actor", null=True, on_delete=models.SET_NULL, related_name='starring_movies')
    actors = models.ManyToManyField("Actor", related_name='actor_movies')


