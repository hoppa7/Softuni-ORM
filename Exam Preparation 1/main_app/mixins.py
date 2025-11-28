from django.db import models
from django.db.models import DateTimeField


class CreationTimeMixin(models.Model):
    creation_date = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
