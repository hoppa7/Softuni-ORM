from django.db import models
from django.db.models.fields import CharField, PositiveIntegerField, TextField, BooleanField, DecimalField


# Create your models here.

class Pet(models.Model):
    name = CharField(
        max_length=40,
    )
    species = CharField(
        max_length=40,
    )

class Artifact(models.Model):
    name = CharField(
        max_length=70,
    )
    origin = CharField(
        max_length=70,
    )
    age = PositiveIntegerField()
    description = TextField()
    is_magical = BooleanField(default=False)

class Location(models.Model):
    name = CharField(
        max_length=100,
    )
    region = CharField(
        max_length=50,
    )
    population = PositiveIntegerField()
    description = TextField()
    is_capital = BooleanField(default=False)

class Car(models.Model):
    model = CharField(
        max_length=40,
    )
    year = PositiveIntegerField()
    color = CharField(
        max_length=40,
    )
    price = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    price_with_discount = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

class Task(models.Model):
    title = CharField(
        max_length=25,
    )
    description = TextField()
    due_date = models.DateField()
    is_finished = BooleanField(default=False)

from .choices import RoomTypeChoices, CharacterChoices


class HotelRoom(models.Model):
    room_number = PositiveIntegerField()
    room_type = CharField(
        max_length=10,
        choices=RoomTypeChoices.choices
    )
    capacity = PositiveIntegerField()
    amenities = TextField()
    price_per_night = DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    is_reserved = BooleanField(
        default=False
    )

class Character(models.Model):
    name = CharField(
        max_length=100,
    )
    class_name = CharField(
        max_length=20,
        choices=CharacterChoices.choices
    )
    level = PositiveIntegerField()
    strength = PositiveIntegerField()
    dexterity = PositiveIntegerField()
    intelligence = PositiveIntegerField()
    hit_points = PositiveIntegerField()
    inventory = TextField()

