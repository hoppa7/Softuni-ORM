from decimal import Decimal

from django.db.models.functions import Round

from .querysets import RealEstateQuerySets, VideoGameQuerySets
from django.db import models
from django.db.models import Count, Max, Min, Avg, F

from .models import *

class RealEstateListingManager(models.Manager.from_queryset(RealEstateQuerySets)):

    def popular_locations(self):
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]


class VideoGameManager(models.Manager.from_queryset(VideoGameQuerySets)):

    def highest_rated_game(self):
        return self.aggregate(Max('rating'))

    def lowest_rated_game(self):
        return self.aggregate(Min('rating'))

    def average_rating(self):
        average_rating = self.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return f"{average_rating:.1f}"