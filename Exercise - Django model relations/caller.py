import os
from datetime import date, timedelta, datetime

import django
from django.db.models import Avg, F, QuerySet
from django.db.models.functions import TruncDate

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *
# Create queries within functions

def show_all_authors_with_their_books():
    authors = Author.objects.prefetch_related("books")
    authors_with_their_books = []

    for author in authors:
        books = author.books.all()
        if not books:
            continue


        titles = ', '.join(book.title for book in books)
        authors_with_their_books.append(f"{author.name} has written - {titles}!")

    return '\n'.join(authors_with_their_books)


def delete_all_authors_without_books():
    Author.objects.filter(books__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist =Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)

def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.order_by('-id')

def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    avg_rating = Review.objects.filter(product=product).aggregate(Avg("rating"))["avg_rating"]
    return avg_rating

def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews

def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True)

def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates() -> str:
    licenses = DrivingLicense.objects.order_by('-license_number')
    return "\n".join(str(l) for l in licenses)

def get_drivers_with_expired_licenses(due_date: date) -> QuerySet[Driver]:

    return Driver.objects.filter(
        license__issue_date__lt=due_date - timedelta(365),
    )


# def calculate_licenses_expiration_dates():
#     exp_dates = DrivingLicense.objects.annotate(
#         new_date = TruncDate(F("issue_date") + timedelta(days=365))
#     ).values("license_number", "new_date").order_by("-license_number")
#
#     for li in exp_dates:
#         print(f"License with number: {li['license_number']} expires on {li['new_date']}!")


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    registration.car = car
    registration.registration_date = datetime.today()
    registration.save()

    car.owner = owner
    car.registration = registration
    car.save()



    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

# def clear_tables():
#     Car.objects.all().delete()
#     Registration.objects.all().delete()
#     Owner.objects.all().delete()

















