from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "owner", "car_details")

    def car_details(self, obj: object):
        try:
            owner_name = obj.owner.name
        except AttributeError:
            owner_name = "No owner"


        try:
            registration = obj.registration.registration_number
        except AttributeError:
            registration = "No registration number"

        return f"Owner: {owner_name}, Registration: {registration}"

    car_details.short_description = "Car Details"