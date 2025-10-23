from django.db import models

class GenreChoices(models.TextChoices):
    FICTION = "F", "Fiction"
    NON_FICTION = "N", "Non-fiction"
    SCIENCE_FICTION = "S", "Science Fiction"
    HORROR = "H", "Horror"