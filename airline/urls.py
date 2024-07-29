"""
URL configuration for flightproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# IMPORT THIS , SO WE CAN SETUP OUR MEDIA URL
from django.conf.urls.static import static
from django.conf import settings
# IMPORT ABOVE , SO WE CAN SETUP OUR MEDIA URL

from . import views
from django.contrib.auth.views import LogoutView  # Import Django's built-in LogoutView

urlpatterns = [

    #Leave as empty string for base url
	path('', views.index, name="index"),

    # register
    path('register/', views.register, name='register'),

    # login
    path('login/', views.loginView, name='login'),
    # logout 
    path('logout/', LogoutView.as_view(), name='logout'),  # Add this line

    # user-details
    path('user-details/', views.userDetailsView, name='user-details'),

    # url for airline page
	path('airline', views.airline, name="airline"),


    # url for view airline details page
    path('view-airline-details/<int:pk>', views.view_airline_details , name='view-airline-details'),

    # url for booking aiirline / cartn page page
	path('book-airline/', views.book_airline, name="book-airline"),

    # url for Checkout page
	path('checkout/', views.checkout, name="checkout"),

    # url for View Booked Flights Orders page
	path('booked-flights/', views.showBookedFlightOrders, name="booked-flights"),
    # url for show booked flight order detai
    path('booked-flight-detail/<int:pk>' , views.showBookedFlightDetails , name='booked-flight-detail'),




    # url for flight Actions page
	path('flight-booking-actions/', views.flightBookingActions, name="flight-booking-actions"),


    # url for FINALIZING CHECKOUT
	path('finalize-checkout/', views.finalizeCheckoutView, name="finalize-checkout"),


    # Other URL patterns
    path('set-currency/', views.set_currency, name='set_currency'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)