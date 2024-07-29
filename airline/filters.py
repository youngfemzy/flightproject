# import django filter
import django_filters
# import custom fields
from django_filters import *
# import django forms 
from django import forms


# import all models in our models.py
from .models import *


# LETS BUILD OUR FILTER FORM

class airlinefilter(django_filters.FilterSet):

    name = CharFilter(field_name='name', lookup_expr = 'icontains', label='' , widget=forms.TextInput(attrs={'placeholder': 'Enter airline name'}))
    # price = CharFilter(field_name='price', lookup_expr = 'lte', label='' , widget=forms.TextInput(attrs={'placeholder': 'Your Budget'}))
     
    takeoffdate = DateFilter(field_name='takeoff_date', lookup_expr = 'gte', label='', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select takeoff date'})  # Placeholder for date field
    )
    origin_city = CharFilter(field_name='origin_city', lookup_expr = 'icontains', label=''  , widget=forms.TextInput(attrs={'placeholder': 'Flight Origin'}))
    destination_city = CharFilter(field_name='destination_city', lookup_expr = 'icontains', label='' , widget=forms.TextInput(attrs={'placeholder': 'Destination'}))
    available_seats = CharFilter(field_name='available_seats', lookup_expr = 'gte', label='' , widget=forms.TextInput(attrs={'placeholder': 'available_seats'}))
    
    takeoff = TypedChoiceFilter(
        field_name='takeoff',
        choices=( (False, 'Available'), (True, 'Not Available') ),
        coerce=lambda x: x == 'True',
        label='',
        widget=forms.Select(attrs={'placeholder': 'Select takeoff'})
    )

    class Meta:

        # we need a minimum of 2 attributes 
        # 1. the modelwe wwant to build the filter for 
        model = Airline
        # 2. which fields we want to filter with
        # field = '__all__'
        fields = '__all__'
        # make sure to exclude images, and othe fields you dontt want to send
        exclude = ['image' , 'takeoff_date', 'name' , 'price', 'origin_city', 'destination_city', 'takeoff', 'seats_used' , 'available_seats', 'capacity']

        # fields_order = ['name', 'takeoff_date']

