import os
from math import remainder

import django
from django.db.models import F, Case, When, ExpressionWrapper, BooleanField, Value
from django.db.models.fields import IntegerField
from django.db.models.functions import Mod

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from main_app.choices import CharacterChoices, FUSION_CLASS_NAME


def create_pet(name: str, species: str):
    pet = Pet.objects.create(name=name, species=species)

    return f"{name} is a very cute {species}!"

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(name=name,
                                       origin=origin,
                                       age=age, description=description,
                                       is_magical=is_magical)
    artifact.save()

    return f"The artifact {artifact.name} is {artifact.age} years old!"

def rename_artifact(artifact: Artifact, new_name: str):
    Artifact.objects.filter(is_magical=True, age__gt=250).update(name=new_name)

def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by("-id")

    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)

def get_capitals():
    capital = Location.objects.values("name").filter(is_capital=True)
    return capital

def new_capital():
    city = Location.objects.first()
    city.is_capital = True
    city.save()

def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    years = Car.objects.aggregate(sum_years=sum('year'))["sum_years"]
    Car.objects.update(price_with_discount=F('price') * int(years) / 100)

def get_recent_cars():
    return Car.objects.filter(year_gt=2020)

def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(f"Task - {t.title} needs to be done until {t.due_date}!"for t in unfinished_tasks)

def complete_odd_tasks():
    Task.objects.annotate(
        remainder=Mod("id", 2)).filter(remainder=1).update(is_finished=True)

def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)
    Task.objects.filter(title=task_title).update(description=encoded_text)



def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    return '\n'.join(f"Deluxe room with number {h.room_number} costs {h.price_per_night}$ per night!" for h in deluxe_rooms)

def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by("id")
    previous_capacity = None

    for room in rooms:
        if room.is_reserved:
            if previous_capacity is None:
                room.capacity += room.id
            else:
                room.capacity += previous_capacity
            room.save()
        previous_capacity = room.capacity

def reserve_first_room():
    first = HotelRoom.objects.first()
    HotelRoom.objects.filter(pk=first.pk).update(is_reserved=True)

def delete_last_room():
    room = HotelRoom.objects.last()
    if not room.is_reserved:
        room.delete()

def update_characters():
    Character.objects.filter(class_name="Mage").update(
        level=F("level") + 3,
        intelligence=F("intelligence") - 7,
    )
    Character.objects.filter(class_name="Warrior").update(
        hit_points=F("hit_points") / 2,
        dexterity=F("dexterity") + 4,
    )
    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character):
    inventory = None

    if first_character.class_name in [CharacterChoices.MAGE, CharacterChoices.SCOUT]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [CharacterChoices.WARRIOR, CharacterChoices.ASSASSIN]:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + " " + second_character.name,
        class_name=FUSION_CLASS_NAME,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory,
    )

    first_character.delete()
    second_character.delete()

def grand_dexterity():
    chars = Character.objects.all()
    chars.update(dexterity=30)

def grand_intelligence():
    chars = Character.objects.all()
    chars.update(intelligence=40)

def grand_strength():
    chars = Character.objects.all()
    chars.update(strength=50)

def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()





