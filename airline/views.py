from django.shortcuts import render, redirect
from django.urls import include
from django.contrib.auth.decorators import login_required

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt  # Temporarily use this if you're having CSRF issues

# IMPORT OUR MODEL
from .models import *

# ---------------IMPORTING OUR FORMS
# IMPORT OUR FILTERS
from .filters import airlinefilter

from django.contrib.auth import authenticate, login, logout  # Correct import
from django.contrib.auth.models import auth

from django.contrib.auth import authenticate
# from django.contrib.auth import login
from .form import *
# ---------------IMPORTING OUR FORMS


# ----------------- IMPORT JSON RESPONSE TO USE JSON RESPONSES
from django.http import JsonResponse
# ------------------ IMPORT JSON , SO WE CAN GET DATA FROM JAVASCRIPT FILES
import json

# TO REQUEST FOR CURRENCY DATA 
import requests
# Create your views here.

# import wikipedia
import wikipediaapi

# TO IMPORT API KEY FOR MAPBOX API
from django.conf import settings

# IMPORTS, SO WE CAN SEARCH BASED ON INPUT FROM INDEX TO AIRLINE.HTML
from django.db.models import Q
from datetime import datetime

# ---------------------------------------------------------------  INDEX / HOMEPAGE VIEW

# VIEW FOR OUR INDEX HOMEPAGE PAGE
def index(request):
    if request.user.is_authenticated:
        # MAKE SURE THE USER LOGGED IN IS ATTRIBUTED TO A CUSTOMER
        try:
            customer = request.user.customer
        # IF THE USER IS NOT A CUSTOMER , THEN MAKE HIM ONE
        except Customer.DoesNotExist:
            customer = Customer.objects.create(customer=request.user)

        context = {'customer': customer}

    # ELSE , IF USER IS NOT LOGGED IN
    # THEN DO NOT ATTRIBUTE  CUSTOMER, TO THE ANONYMOUS USER
    else:
        context = {}
    

    return render(request, 'airline/index.html', context)






# --------------------------------- REGISTER VIEW ++++++++++++++++++++++++++++

def register(request):
    if request.user.is_authenticated:
        return redirect('../')  # Redirect to the homepage if user is authenticated
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('../')  # Redirect to a success page or home page
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})

# --------------------------------- REGISTER VIEW ENDS -------------------------------


# --------------------------------- login VIEW ++++++++++++++++++++++++++++

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to the homepage if user is authenticated
    if request.method == 'POST':
        loginform = LoginForm(request, data=request.POST)

        if loginform.is_valid():
            #  get value inputted by user for username and password
            username = request.POST.get('username')
            password = request.POST.get('password')
            # now authenticate , for which user is logging in
            # we do this by matching entered input , with records in our database 
            # if username maches anyone in our database
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(user)
                auth.login(request, user)
                return redirect('../')  # Redirect to a success page or home page        
    else:
        loginform = LoginForm()

    return render(request, 'user/login.html', {'loginformContext': loginform})

# --------------------------------- login VIEW ENDS -------------------------------





# --------------------------------- User Details VIEW -------------------------------
@login_required
def userDetailsView(request):
    user = request.user
    customer, created = Customer.objects.get_or_create(customer=user)
  
    if request.method == 'POST':
        print('called')
        customerform = customerForm(request.POST, instance=customer)
        if customerform.is_valid():
            customerform.save()
            # return redirect('some-success-url')  # Redirect to a success page
    else:
        # if we are not posting , then just show this customers personal details
        customerform = customerForm(instance=customer)

    context = {'customerformContext': customerform}
    return render(request, 'user/user-details.html', context)

# --------------------------------- User Details VIEW ENDS -------------------------------










# --------------------------------------------------------------- AIRLINE / SHOP PAGE VIEW


def airline(request):
    # Get all airplanes that have not taken off
    airplane = Airline.objects.filter(takeoff=False)

    # ************************* GET SEARCH DATA PASED FROM INDEX.HTML
    # Get the search parameters from the GET request
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    seats = request.GET.get('seats')
    date = request.GET.get('date')
    flightname = request.GET.get('flightname')

    # Apply the filters
    if origin:
        airplane = airplane.filter(origin_city__icontains=origin)
    if destination:
        airplane = airplane.filter(destination_city__icontains=destination)
    if seats:
        airplane = airplane.filter(available_seats__gte=seats)
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
        airplane = airplane.filter(takeoff_date__date__lte=date)
    if flightname:
        airplane = airplane.filter(name__icontains=flightname)

    # ************************* GET SEARCH DATA PASED FROM INDEX.HTML ENDS

    # Apply filters
    myairlineFilter = airlinefilter(request.GET, queryset=airplane)
    airplanefilter = myairlineFilter.qs

    context = {
        'airplane_context': airplane,
        'myairlineFilterContext': myairlineFilter,
        'airplanes_with_converted_prices': [
            {
                'airplane': each_airplane,
                'converted_price': each_airplane.price * request.session.get('exchange_rate', 1),
                'currency_code': request.session.get('currency_code', 'USD'),
            } for each_airplane in airplanefilter
        ],
    }
    return render(request, 'airline/airline.html', context)


# ++++++++++++++++++++++++++++++++++++++--------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++--------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++--------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Function to get weather information from OpenWeatherMap
def get_weather(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data.get('main'):
        return {
            'temperature': data['main']['temp'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'cloudiness': data['clouds']['all'],
            'global_precipitation': data['rain']['1h'] if 'rain' in data else 0,
            'description': data['weather'][0]['description'],
        }
    return {}



# Function to get detailed Wikipedia information
def get_wikipedia_details(city_name):
    # Specify a user agent to identify your application
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='airline/1.0 (youngfemzymie@gmail.com)'  # Use your app's name and your email
    )
    page = wiki_wiki.page(city_name)
    if page.exists():
        return {
            'summary': page.summary,
            'full_text': page.text[:0],  # Adjust the number of characters you want to display
            'url': page.fullurl
        }
    return {
        'summary': 'No information available.',
        'full_text': '',
        'url': ''
    }


# FUNCTION TO CHANGE CITY NAME TO CO ORDINATES , LONGITUDE AND LATITUDE 
# Function to get coordinates of a city from OpenStreetMap
def get_coordinates(city_name):
    api_key = 'a3912260a0c2402f8f10ebaeeeef6692'  # Replace with your OpenCage API key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and data['results']:
            return (float(data['results'][0]['geometry']['lat']), float(data['results'][0]['geometry']['lng']))
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return (None, None)

# --------------------------------------------------------------- VIEW SINGLE AIRLINE PAGE VIEW
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# View function to display details of a specific airline
def view_airline_details(request, pk):
    # Fetch the airline object using the primary key (pk)
    airline = Airline.objects.get(id = pk)

    print(airline.origin_city) 
    # Fetch currency and exchange rate from session
    currency_code = request.session.get('currency_code', 'USD')
    exchange_rate = request.session.get('exchange_rate', 1)

    # Calculate the converted price
    converted_price = airline.price * exchange_rate


    # Get coordinates for origin and destination cities
    origin_coords = get_coordinates(airline.origin_city)
    destination_coords = get_coordinates(airline.destination_city)
    print(origin_coords)


    # Convert coordinates to JSON strings for use in JavaScript
    origin_coords_json = json.dumps(origin_coords)
    destination_coords_json = json.dumps(destination_coords)

    # print(origin_coords)


    # Get weather information and Wikipedia summary
    weather_api_key = '8fda512f20bdba35ab6d600492678c6c'  # Replace with your OpenWeatherMap API key
    weather_info = get_weather(airline.destination_city, weather_api_key)
    #  wikipedia_summary = get_wikipedia_summary(airline.destination_city)
    # Fetch Wikipedia details for destination city
    wikipedia_details = get_wikipedia_details(airline.destination_city)



    # Prepare context dictionary to pass data to the template
    context={
        'view_airline_context': airline , 
        'view_airline_converted_price_context': converted_price,

        
        'origin_coords_json': origin_coords_json, # JSON string of origin coordinates
        'destination_coords_json': destination_coords_json, # JSON string of destination coordinates
        'weather_info': weather_info,
        # 'wikipedia_summary': wikipedia_summary,
        'wikipedia_details': wikipedia_details,
            
        }
    return render(request, 'airline/view-airline-details.html', context)



# --------------------------------------------------------------- VIEW SINGLE AIRLINE PAGE VIEW ENDS



# ++++++++++++++++++++++++++++++++++++++--------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++--------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++--------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++















# --------------------------------------------------------------- BOOK AIRLINE PAGE VIEW


# VIEW FOR OUR BOOK AIRLINE PAGE
# SAME AS A CART PAGE
def book_airline(request):
     
    # code for display cart item in cart page

     # --------------- if the user is authenticated

     if request.user.is_authenticated:

          # access the relationship between the user & customer
          customer = request.user.customer

          # get the customers  order, OrderFlight  , create one if it doesnt exist
          # the order we are going to get, is going to have an attribute of our loggin & customer i.e customer:customer
          order , created = OrderFlight.objects.get_or_create(customer = customer, complete = False)

          # get all order items in our particular ORDER FLIGHT
          cartitem = order.orderitem_set.all()

          cartIconShowQuantity = order.get_total_seats_booked

          
     
     # -----------------IF USER IS NOT AUTHENTICATED      
     else:
          cartitem = []
          order = {'get_all_order_total':0, 'get_total_seats_booked':0}
          cartIconShowQuantity = order['get_total_seats_booked']



# ------------------------- TO FETCH CONVERTED PRICE FOR CART PAGE


     # Fetch currency from session
     currency_code = request.session.get('currency_code', 'USD')
     exchange_rate = request.session.get('exchange_rate', 1)

     # Initialize list for cart items with converted prices
     cartitems_with_converted_prices = []

     # Initialize a variable to hold the total converted order cost
     total_converted_order_cost = 0

     for each_cartitem in cartitem:
        # Get the original price of the airline ticket
        original_price = each_cartitem.airline.price
        # Calculate the converted price using the exchange rate
        converted_price = original_price * exchange_rate
        # Calculate the total converted price for the cart item
        total_converted_price = each_cartitem.get_cart_item_total * exchange_rate

        # Add the total converted price to the total converted order cost
        total_converted_order_cost += total_converted_price
        #store it in a 
        # Store the selected currency and rate in the session
        request.session['total_converted_order_cost'] = total_converted_order_cost
            

        cartitems_with_converted_prices.append({
            'cartitem': each_cartitem,
            'converted_price': converted_price,
            'total_converted_price': total_converted_price,
            'currency_code': currency_code,
            
        })


    # Prepare the context dictionary to pass data to the template
     context = {
          'cartitemcontext': cartitem, 
          'ordercontext': order , 
          'cartIconShowQuantity': cartIconShowQuantity , 
          'cartitem_price_converted_context': cartitems_with_converted_prices,
          'currency_code': currency_code,  # Ensure currency code is passed
          
          'total_converted_order_cost': total_converted_order_cost,
        }
     
    # Render the template with the context data
     return render(request, 'airline/book-airline.html', context)

















# ------------------------------------------------ START OF CHECKOUT PAGE VIEW


# --------------------------------------------------------------- VIEW FOR OUR CHECKOUT PAGE


# VIEW FOR OUR CHECKOUT PAGE
def checkout(request):
     # code for display cart item in CHECKOUT page
     if request.user.is_authenticated:

          customer = request.user.customer

          # pass in checkout form from form.py
          checkoutform = checkoutForm()



          # pass everything we want to send to frontpage into context dictionary
          context = {'customerContext': customer}
          return render(request, 'airline/checkout.html', context)
     
     else:
          
          # Redirect to the previous page or homepage
          return redirect(request.META.get('HTTP_REFERER', '/'))










# ------------------------------------------------- FINALIZE CHECKOUT VIEW



def finalizeCheckoutView(request):
    if request.method == 'POST':
        
          # Transform the JSON string into its raw form
          checkoutdata = json.loads(request.body)
          print("Raw request body:", request.body)
          
          # Extract data
          checkoutproductId = checkoutdata.get('checkoutproductId')
          action = checkoutdata.get('action')
          print("Checkout ID:", checkoutproductId, "Action:", action)

          # Query the customer
          customer = request.user.customer

          # Get or create the order for the customer
          order , created = OrderFlight.objects.get_or_create(customer = customer, complete = False)
          print(order.id)
          # Get the items in the order
          orderitem  = OrderItem.objects.filter(order=order)
          print("Order Items:", orderitem)

          # IF THE ACTION IS CHECK OUT-----------------------------
          if action == 'checkout':

               # update our order items
               for eachorderitem in orderitem:
                    # UPDATE AIRLINE SEAT CAPACITY CODE START
                    # print(eachorderitem.airline.seats_used)                
                    # Increment seats_used
                    eachorderitem.airline.seats_used += eachorderitem.quantity

                    # print(eachorderitem.airline.seats_used)
                    eachorderitem.airline.save()

                    # ---- UPDATE AVAILABLE SEATS OF EACH AIRLINE
                    eachorderitem.airline.available_seats = eachorderitem.airline.capacity - eachorderitem.airline.seats_used
                    eachorderitem.airline.save(update_fields=['available_seats'])
                    # UPDATE AIRLINE SEAT CAPACITY CODE ENDS

                   # Complete the order
                    order.totalbill = order.get_all_order_total
                    order.totalseatsbooked = order.get_total_seats_booked
                    print (order.totalbill)
                    order.complete = True
                    order.save()

    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

          

# ------------------------------------------------ END OF CHECKOUT PAGE VIEW











# ---------------------------  VIEW FOR ADDING TO CART , USING JSON RESPONSES , IMPORTING FROM JS & MORE --------------------------------
def flightBookingActions(request):
     # WE SENT SOME DATA THROUGH JSON STRINGIFY, IN CART.JS
    

     # WE NEED TO TRANSFORM THIS STRING ,INTO ITS RAW FORM , SO WE CAN USE IT
      # first We Import Json , On the top 
     #  Then
     data = json.loads(request.body)
     print("Raw request body:", request.body)
     # now lets get our raw data from front end, its been saved in data variable
     productId = data['productId']
     action = data['action']
     print("Product ID:", productId, "Action:", action)

     # NOW THAT WE HAVE OUR DETAILS
     # LETS START WORK WITH THEM
     
     # --------------- if the user is authenticated
     if request.user.is_authenticated:
          # ORDER & ADD TO CART , BASED ON WHICH CUSTOMER CLICKED THE BUTTON
          # query the customer
          customer = request.user.customer


          # query or get the airline
          airline = Airline.objects.get(id = productId)

          # get the order of this customer, that has the condition complete = false
          # get the customers  order, OrderFlight  , create one if it doesnt exist
          # the order we are going to get, is going to have an attribute of our loggin & customer i.e customer:customer
          order , created = OrderFlight.objects.get_or_create(customer = customer, complete = False)

          # now get the cart items inside the order
          # we would use get or create , -- for this because if the cart item already exists , we want to update the price
          orderitem , created = OrderItem.objects.get_or_create(order = order, airline = airline)

          # if butto clicked is add to cart
          if action == 'add-to-cart':
               orderitem.quantity += 1
          elif action == 'remove-from-cart':
               orderitem.quantity -= 1
          
          orderitem.save()

          if orderitem.quantity <= 0 :
               orderitem.delete()
               
          return JsonResponse( productId, safe=False)
      
     # Else if user is not authenticated
     else:
          orderitem = []
          order = {'get_all_order_total':0, 'get_total_seats_booked':0}
          return redirect('registration/login.html')  # Adjust the login URL as needed






















# ---------------------------- SHOW BOOKED FLIGHTS PAGE VIEW
def showBookedFlightOrders(request):


    # --------------- if the user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        
        if request.user.is_staff:
            # If the user is a staff member, get all completed orders
            completed_orders = OrderFlight.objects.filter(complete=True)
        else:   
            completed_orders = OrderFlight.objects.filter(customer = customer, complete = True)
            print(completed_orders)

        # Initialize converted_total_bill in case there are no orders
        converted_total_bill = 0
        # Initialize an empty list to hold orders with their converted total bills
        orders_with_converted_bills = []

        # Check if user has any completed orders
        if completed_orders.exists():
            
            # Fetch currency and exchange rate from session
            exchange_rate = request.session.get('exchange_rate', 1)

            for eachCompletedOrder in completed_orders:
                converted_total_bill = eachCompletedOrder.totalbill * exchange_rate
                print(converted_total_bill)
                
                orders_with_converted_bills.append({
                'order': eachCompletedOrder,
                'converted_total_bill': converted_total_bill,
                })

            # Calculate the converted price
                
            # converted_price = completed_orders.totalbill * exchange_rate

            # Prepare the context dictionary to pass to the template
            context = {'orders_with_converted_billsContext': orders_with_converted_bills}


        else:
            print("No completed orders found")
            # If there are no completed orders, provide an empty context
            context = {
                'orders_with_converted_bills': [],
            }

            
        # Render the template and pass the context
        return render(request, 'airline/booked-flights.html', context)

    # Else if user is not authenticated
    else:
    
        # debug
        print("Anonymous User")
        # Redirect to the previous page or homepage
        return redirect(request.META.get('HTTP_REFERER', '/'))

# ---------------------------- SHOW BOOKED FLIGHTS PAGE VIEW ENDS


# ---------------------------- SHOW BOOKED FLIGHTS DETAILS PAGE VIEW

def showBookedFlightDetails(request, pk):

     # --------------- if the user is authenticated
     if request.user.is_authenticated:

          customer = request.user.customer

          # query the logged in users Order Database Table
          order = OrderFlight.objects.get( id = pk , customer = customer)
          print(order)
          # Filter The customers order items , and select only the ones that belongs to this user
          orderitem = OrderItem.objects.filter(order = order)
          print(orderitem)

          
          # Fetch currency and exchange rate from session
          exchange_rate = request.session.get('exchange_rate', 1)

          for eachorderitem in orderitem:
               print(eachorderitem.airline.price)
               # Now Lets Convert The Price Currency To Selected Currency
               converted_price = eachorderitem.airline.price * exchange_rate

          # lets pass everything into context
          context = {'orderitemcontext': orderitem , 'ordercontext': order , 'converted_price':converted_price}

          return render(request, 'airline/booked-flight-detail.html', context)
     
     
     else:
          return render(request, 'airline/booked-flight-detail.html')




# ---------------------------- SHOW BOOKED FLIGHTS DETAILS PAGE VIEW ENDS


















































def set_currency(request):
    # URL for fetching currency exchange rates
    url = 'https://v6.exchangerate-api.com/v6/fff75be91385bc0fd4cf9b4c/latest/USD'
    
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data['result'] == 'success':
        exchange_rates = data['conversion_rates']
    else:
        exchange_rates = {}
    
    # Default currency
    default_currency = 'USD'
    default_rate = exchange_rates.get(default_currency, 1)
    
    # Check if a currency is selected
    selected_currency = request.GET.get('currency', default_currency)
    selected_rate = exchange_rates.get(selected_currency, default_rate)
    
    # Store the selected currency and rate in the session
    request.session['currency_code'] = selected_currency
    request.session['exchange_rate'] = selected_rate
    
    # Redirect to the previous page or homepage
    return redirect(request.META.get('HTTP_REFERER', '/'))












# # ---------------------------- SHOW BOOKED FLIGHTS PAGE VIEW
# def showBookedFlightOrders(request):


#      # --------------- if the user is authenticated
#      if request.user.is_authenticated:
#           customer = request.user.customer
#           print(customer)

#           completed_orders = OrderFlight.objects.filter(customer = customer, complete = True)
#           print(completed_orders)

#           # Create an empty dictionary to hold orders and their associated items
#           orders_with_items = {}

#           # Loop through each completed order
#           for order in completed_orders:
#                # Fetch all items associated with the current order
#                order_items = order.orderitem_set.all()
#                print(order_items)  # Print items for debugging

#                # Store the order and its items in the dictionary
#                orders_with_items[order] = order_items

#           # Prepare the context dictionary to pass to the template
#           context = {'orders_with_items': orders_with_items}

#           # Render the template and pass the context
#           return render(request, 'airline/booked-flights.html', context)



#      # Else if user is not authenticated
#      else:
      
#           orders_with_items = []
#           # debug
#           print("Anonymous User")
#           return render(request, 'airline/booked-flights.html')






















