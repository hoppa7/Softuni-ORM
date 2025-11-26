from abc import ABC, abstractmethod
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey
from .fields import StudentIDField, MaskedCreditCardField


# Create your models here.
#1
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True

class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)

class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)

class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)

class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)

class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)

class ViperAssassin(Assassin):
    venomous_strike_mastery = models.CharField(max_length=100)
    venomous_bike_ability = models.CharField(max_length=100)

class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)

class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)

class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)

#2
class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

class Message(models.Model):
    sender = ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="sent_messages")
    receiver = ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def reply_to_message(self, reply_content: str):
        new_message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )

        new_message.save()

        return new_message

    def forward_message(self, receiver: UserProfile):
        new_message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )

        new_message.save()
        return new_message

#3
class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


#4
class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField(max_length=20)

#5
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Room(models.Model):
    hotel = ForeignKey("Hotel", on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"

class BaseReservation(models.Model):
    room = ForeignKey("Room", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def reservation_period(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        return self.room.price_per_night * self.reservation_period()

    def get_overlapping(self, start_date, end_date):
        return self.__class__.objects.filter(
            room=self.room,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

    @property
    def is_available(self) -> bool:
        return not self.get_overlapping(self.start_date, self.end_date).exists()

    @property
    def reservation_type(self):
        raise NotImplemented

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f"{self.reservation_type} reservation for room {self.room.number}"

class RegularReservation(BaseReservation):
    @property
    def reservation_type(self) -> str:
        return "Regular"



class SpecialReservation(BaseReservation):

    @property
    def reservation_type(self) -> str:
        return "Special"

    def extend_reservation(self, days: int):
        new_end_date = self.end_date + timedelta(days=days)
        check_overlap = self.get_overlapping(self.start_date, new_end_date)

        if check_overlap.exists():
            raise ValidationError("Error during extending reservation")

        self.end_date = new_end_date
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"




