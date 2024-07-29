from django.contrib import admin


# import our model
from .models import *


# Register your models here.
admin.site.register(Customer)
admin.site.register(Airline)
admin.site.register(OrderFlight)
admin.site.register(OrderItem)