# context_processors.py
from .models import *
from .filters import airlinefilter
# your_app/context_processors.py


def currency_and_order_info(request):
    # Get currency and exchange rate from session
    currency_code = request.session.get('currency_code', 'USD')
    exchange_rate = request.session.get('exchange_rate', 1)

    # Initialize context variables
    cartIconShowQuantity = 0
    order = {'get_all_order_total': 0, 'get_total_seats_booked': 0}
    airplanes_with_converted_prices = []
    cartitems_with_converted_prices = []
    checkoutitems = []
    # initialize overall total which is converted to selected currency
    total_converted_order_cost = 0

    # Check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderFlight.objects.get_or_create(customer=customer, complete=False)
        cartIconShowQuantity = order.get_total_seats_booked







# ------------------------------- GENERAL CONTEXT FOR CART PAGE ---------------------------------------------------------


        # Get cart items and calculate converted prices
        cartitem = order.orderitem_set.all()



        # for each cart item is inside a particular order
        for each_cartitem in cartitem:
            original_price = each_cartitem.airline.price
            converted_price = original_price * exchange_rate
            total_converted_price = each_cartitem.get_cart_item_total * exchange_rate
            # calculate Total Order Bill which has been converted
            total_converted_order_cost += total_converted_price

            cartitems_with_converted_prices.append({
                'cartitem': each_cartitem,
                'converted_price': converted_price,
                'total_converted_price': total_converted_price,
                'currency_code': currency_code,
            })
            # print(cartitems_with_converted_prices)

        request.session['total_converted_order_cost'] = total_converted_order_cost

# ------------------------------- GENERAL CONTEXT FOR CART PAGE---------------------------------------------------------



# ------------------------------- GENERAL CONTEXT FOR CHECKOUT PAGE ---------------------------------------------------------

        customer = request.user.customer
        # Get checkout items

        checkoutitems_queryset  = order.orderitem_set.all()

        for each_cartitem in checkoutitems_queryset :
            total_converted_price = each_cartitem.get_cart_item_total * exchange_rate

            checkoutitems.append({
            'total_converted_price': total_converted_price,
            'airline': each_cartitem.airline,
            'Seats_used': each_cartitem.quantity,
            'currency_code': currency_code,
            })
            # print(checkoutitems)


# ------------------------------- GENERAL CONTEXT FOR CHECKOUT PAGE ---------------------------------------------------------








# ------------------------------- GENERAL CONTEXT FOR AIRLINE PAGE---------------------------------------------------------

    # Fetch airplanes and convert prices
    airplane = Airline.objects.all()
    # Convert prices for airplanes & airplane filters
    myairlineFilter = airlinefilter(request.GET, queryset=airplane)
    airplanefilter = myairlineFilter.qs

    # Convert prices for airplanes
    for each_airplane in airplanefilter:
        original_price = each_airplane.price
        converted_price = original_price * exchange_rate
        airplanes_with_converted_prices.append({
            'airplane': each_airplane,
            'converted_price': converted_price,
            'currency_code': currency_code,
        })


# ------------------------------- GENERAL CONTEXT FOR AIRLINE PAGE ENDS---------------------------------------------------------






    context = {
        'cartIconShowQuantity': cartIconShowQuantity,
        'cartitems_with_converted_prices': cartitems_with_converted_prices,
        'ordercontext': order,
        'airplanes_with_converted_prices': airplanes_with_converted_prices,
        'total_converted_order_cost': total_converted_order_cost,
        'currency_code': currency_code,
        'checkoutitems': checkoutitems,

    }

    
    return context
