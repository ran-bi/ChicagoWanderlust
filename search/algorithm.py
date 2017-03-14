
from .util.scrapers import airbnb, booking
from .util.routes import select_by_routes, ATTRACTIONS
from .util.yelp_filter import get_filter_l
from .util.safety_filter import filter_danger
from .util.final_format import get_final_output
import datetime
import os

def recommend(data):
    valid_data = check_user_input(data)

    if not valid_data['valid']:
        context = {'error': valid_data['error']}
        return (False, context)
    else:
        CHECKIN = valid_data['checkin']
        CHECKOUT = valid_data['checkout']
        DAYS = valid_data['days']
        PRICEMIN = valid_data['pricemin']
        PRICEMAX = valid_data['pricemax']
        TRANSIT_MODE = valid_data['transit_mode']
        PREFS = valid_data['prefs']

    try:
        AIRBNB = airbnb(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
        print(AIRBNB)
    except:
        context = {'error':'Please check internet connection'}
        return (False, context)

    try:
        BOOKING = booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
        print(BOOKING)
    except:
        context = {'error': 'Please check internet connection and make sure Chrome webderiver works properly'}
        return (False, context)

    LOCATIONS = AIRBNB.append(BOOKING, ignore_index = True)

    try:
        loc_routes = select_by_routes(PREFS, LOCATIONS, DAYS, TRANSIT_MODE, -1)
        print(loc_routes)
    except:
        context = {'error':'Please use another Google API Key in routes.py'}
        return (False, context)
    
    try:
        loc_lst = get_filter_l(loc_routes, LOCATIONS, -1)
        print(loc_lst)
    except:
        context = {'error':'Please check Yelp API Key'}
        return (False, context)

    loc = filter_danger(loc_lst, LOCATIONS, loc_routes)

    if loc == []:
    	context = {'error': 'No search result matching your input. Please refine your input.'}
    	return (False, context)
    else:
    	context = get_final_output(loc, loc_routes, ATTRACTIONS, LOCATIONS)
    	return (True, context)

def check_user_input(data):
    '''
    Check Validity of user input.
    '''
    rv ={}
    if not check_days(data):
        return {'valid': False,
                'error':'Please input valid dates'}
    else:
        checkin, checkout, days = check_days(data)

    if not check_price_range(data):
        return {'valid': False,
                'error': 'Please input valid price range'}
    else:
        pricemin, pricemax = check_price_range(data)
    
    prefs = check_prefs(data)
    rv = {'valid': True,
          'checkin': checkin,
          'checkout': checkout,
          'days': days,
          'pricemin': pricemin,
          'pricemax': pricemax,
          'transit_mode': data['trans'],
          'prefs':prefs}
    return rv

def check_days(data):
    '''
    Check date input validity:
    - Checkin date must be within 50 days from today.
    - Checkin date must not be past date.
    - Checkout date must be later than checkin date. 
    - If checkout within two days, plan one day routes. (day=1)
    - If checkout after two days, plan two day routes. (day=2)
    '''

    checkin = data['checkin']
    checkout = data['checkout']

    if not checkin or not checkout:
        return False

    delta = checkout - checkin
    days = delta.days
    delta_today = (checkin - datetime.date.today()).days

    if delta_today < 0 or delta_today > 365:
        return False
    elif days > 0 and days <= 2:
        return (checkin, checkout, 1)
    elif days > 2 and days <= 10:
        return (checkin, checkout, 2)
    else:
        return False

def check_price_range(data):
    '''
    Check price range validity:
    - Upper bound must be higher than lower bound.
    '''

    minprice = data['pricemin']
    maxprice = data['pricemax']
    if not minprice or not maxprice:
        return False
    if minprice >= maxprice:
        return False
    else:
        return (minprice, maxprice)

def check_prefs(data):
    '''
    Check attraction preferences input validity:
    - Return a list of preference criteria. The first element in the list is of the highest priority.
    '''
    raw_prefs = [data['attraction_1'], data['attraction_2'], data['attraction_3']]
    prefs= []
    for pref in raw_prefs:
        if pref != 'None':
            if pref not in prefs:
                prefs.append(pref)

    return prefs
