from django.db import models

# import the django default user model
from django.contrib.auth.models import User
# Create your models here.

# import timezone , so we can calculate ,if airline is supposed to take off yet
from django.utils import timezone



# ------------ CUSTOMER MODEL


class Customer(models.Model):
    # the logic below means 1 user is 1 customer, 1 to 1 relationship, a user can only have one customer , viceversa
    customer = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)


    # this shows customers name in django admin dashboard
    def __str__(self):
        return self.customer.username
    

# ------------ CUSTOMER MODEL ENDS











# ------------ AIRLINE / AIRPLANE DETAILS MODEL

class Airline(models.Model):
    # the logic below 
    name = models.CharField(max_length=200)
    price = models.FloatField(max_length=200)
    takeoff_date = models.DateTimeField(null=True, blank=True)
    origin_city = models.CharField(max_length=200, null=True, blank=True)
    destination_city = models.CharField(max_length=200, null=True, blank=True)
    seats_used = models.IntegerField(default=0, null=True, blank=True)
    capacity = models.IntegerField(default=240, null=True, blank=True)
    available_seats = models.IntegerField(default=0, null=True, blank=True)
    takeoff = models.BooleanField(default=False, null=True, blank=True)

    image = models.ImageField(null=True, blank=True)
    
    # this shows Airline name in django admin dashboard
    def __str__(self):
        return self.name
    
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    
    def save(self, *args, **kwargs):
        self.available_seats = self.capacity - self.seats_used

         # Check if takeoff_date has passed
        if self.takeoff_date and self.takeoff_date < timezone.now():
            self.takeoff = True
         # Check if takeoff_date has not yet passed
        if self.takeoff_date and self.takeoff_date > timezone.now():
            self.takeoff = False
        
        # Check if seats_used is greater than or equal to capacity
        if self.seats_used >= self.capacity:
            self.takeoff = True
        super(Airline, self).save(*args, **kwargs)


# ------------ AIRLINE / AIRPLANE DETAILS MODEL ENDS

















# ------------ FLIGHT ORDER / FLIGHT BOOKING DETAILS MODEL

class OrderFlight(models.Model):
    # the logic below means 1 user is 1 customer, 1 to 1 relationship, a user can only have one customer , viceversa
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL ,null=True, blank=True)
    dateordered = models.DateTimeField(auto_now_add=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    totalbill = models.IntegerField(default=0, null=True, blank=True)
    currency_code = models.CharField(max_length=10,null=True, blank=True)
    totalseatsbooked = models.IntegerField(default=0, null=True, blank=True)
    

    # this shows ORDER ID in django admin dashboard
    def __str__(self):
        return str(self.id)
    
    @property
    def get_all_order_total(self):
        # get all order items in our particular ORDER FLIGHT
        cartitem = self.orderitem_set.all()
        # CALCULATION FOR TOTAL PRICE OF FLIGHT ORDER 
        totalOrderBill = sum([item.get_cart_item_total for item in cartitem])
        return totalOrderBill
# ------------ FLIGHT ORDER / FLIGHT BOOKING DETAILS MODEL ENDS
    
    @property
    def get_total_seats_booked(self):
        # get all order items in our particular ORDER FLIGHT
        cartitem = self.orderitem_set.all()
        # CALCULATION FOR TOTAL PRICE OF FLIGHT ORDER 
        totalSeatsBooked = sum([item.quantity for item in cartitem])
        return totalSeatsBooked
# ------------ FLIGHT ORDER / FLIGHT BOOKING DETAILS MODEL ENDS

















# ------------ FLIGHT ADD TO CART DETAILS MODEL

class OrderItem(models.Model):
    # the logic below means, a 1 Airline can have multiple add to cart, added to it
    airline = models.ForeignKey(Airline, on_delete=models.SET_NULL ,null=True, blank=True)
    # the logic below means, a 1 Order can have multiple items
    order = models.ForeignKey(OrderFlight, on_delete=models.SET_NULL ,null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added_to_cart = models.DateTimeField(auto_now_add=True)


    # this shows customers name in django admin dashboard
    def __str__(self):
        return self.airline.name
    
    # CODE TO SET TOTAL PRICE FOR EACH CART ITEM
    @property
    def get_cart_item_total (self):
        cartTotal = self.airline.price * self.quantity
        return cartTotal
        # NOW THAT WE HAVE OUT TOTAL RETURNED , WE CAN RENDER THIS DIRECTLY TO OUR TEMPLATE HTML
    
    
    
    
# ------------ FLIGHT ADD TO CART DETAILS MODEL ENDS