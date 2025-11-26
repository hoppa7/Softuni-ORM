from decimal import Decimal
from .querysets import RealEstateQuerySets
from django.db import models
from django.db.models import Count

from .models import *

class RealEstateListingManager(models.Manager.from_queryset(RealEstateQuerySets)):

    def popular_locations(self):
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]