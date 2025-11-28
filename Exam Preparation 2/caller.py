import os
import django
from django.db.models import Q, Count, Avg, Max, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *
# Create queries within functions
from datetime import date


def get_directors(search_name=None, search_nationality=None):
    if search_name is not None and search_nationality is not None:
        matches = Director.objects.filter(Q(full_name__icontains=search_name)
                                    & Q(nationality__icontains=search_nationality)).order_by('full_name')
    elif search_name is not None:
        matches = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')

    elif search_nationality is not None:
        matches = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')

    else:
        return ""

    if not matches:
        return ""

    return '\n'.join(
        [f"Director: {m.full_name}, nationality: {m.nationality}, experience: {m.years_of_experience}"
         for m in matches])

def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."

def get_top_actor():
    top_actor = Actor.objects.annotate(num_movies=Count('actor_movies'), avg_rating=Avg('starring_movies__rating')).order_by('-num_movies', 'full_name').first()
    return f"Top Actor: {top_actor.full_name}, starring in movies: {', '.join(m.title for m in top_actor.starring_movies.all())}, movies average rating: {top_actor.avg_rating:.1f}"



def get_actors_by_movies_count():
    top_actors = Actor.objects.annotate(num_movies=Count('actor_movies')).order_by('-num_movies', 'full_name')[:3]
    return '\n'.join([f"{act.full_name}, participated in {act.num_movies} movies" for act in top_actors])


def get_top_rated_awarded_movie():
    top_movie =  Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not top_movie:
        return ""

    cast = top_movie.actors.all().order_by('full_name')

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'


    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating}. Starring actor: {starring_actor}. Cast: {', '.join(a.full_name for a in cast)}."
print(get_top_rated_awarded_movie())

def increase_rating():
    classic_movies = Movie.objects.filter(Q(is_classic=True) & Q(rating__lt=10))
    updated_count = classic_movies.update(rating=F('rating') + 0.1)

    if updated_count == 0:
        return "No ratings increased."

    return f"Rating increased for {updated_count} movies."




