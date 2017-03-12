
from .util.scrapers import airbnb, booking
from .util.routes import select_by_routes, ATTRACTIONS
from .util.yelp_filter import get_filter_l
from .util.safety_filter import filter_danger
from .util.final_format import get_final_output
import datetime
import os

def foof(data):
    valid_data = check_user_input(data)

    if not valid_data['criteris_met']:
        context = valid_data['context']
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
        context = 'Please check internet connection'
        return (False, context)

    try:
        BOOKING = booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
        print(BOOKING)
    except:
        context = 'Please check internet connection and make sure Chrome webderiver works properly'
        return (False, context)

    LOCATIONS = AIRBNB.append(BOOKING, ignore_index = True)

    try:
        loc_routes = select_by_routes(PREFS, LOCATIONS, DAYS, TRANSIT_MODE, -1)
        print(loc_routes)
    except:
        context = 'Please use another Google API Key in routes.py'
        return (False, context)
    
    try:
        loc_lst = get_filter_l(loc_routes, LOCATIONS, -1)
        print(loc_lst)
    except:
        context = 'Please check Yelp API Key'
        return (False, context)

    loc = filter_danger(loc_lst, LOCATIONS, loc_routes)
    print(loc)
    context = get_final_output(loc, loc_routes, ATTRACTIONS, LOCATIONS)
    
    if context == []:
        return (False, 'No search result matching your input. Please refine your input.')
    
    else:
        return (True, context)

def check_user_input(data):
    '''
    Check Validity of user input.
    '''
    rv ={}
    if not check_days(data):
        return {'criteris_met': False,
                'context':'Please input valid dates'}
    else:
        checkin, checkout, days = check_days(data)

    if not check_price_range(data):
        return {'criteris_met': False,
                'context': 'Please input valid price range'}
    else:
        pricemin, pricemax = check_price_range(data)
    
    prefs = check_prefs(data)
    rv = {'criteris_met': True,
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
    delta = checkout - checkin
    days = delta.days
    delta_today = (checkin - datetime.date.today()).days

    if delta_today < 0 or delta_today > 50:
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


'''
{'attraction_3': 'None', 'pricemax': 300, 'attraction_2': 'None', 'trans': 'driving', 'attraction_1': 'None', 'checkout': datetime.date(2017, 1, 1), 'pricemin': 20, 'checkin': datetime.date(2017, 1, 1)
'''


'''
default_output = {'BookingLink1': 'https://www.airbnb.com/rooms/15926166',
'BookingLink2': 'www.booking.com/hotel/us/omni-chicago.en-gb.html?label=gen173nr-1FCAQoggJCDWNpdHlfMjAwMzMxNzNIM2IFbm9yZWZyBXVzX2lsiAEBmAEuuAEKyAEF2AEB6AEB-AELqAID;sid=28e69b52be3281ae5b7ba8b2459908ad;ucfs=1;highlighted_blocks=137190405_86519026_2_0_0;all_sr_blocks=137190405_86519026_2_0_0;room1=A%2CA;hpos=38;dest_type=city;dest_id=20033173;srfid=4a03b0b55938edff661815f856f13538dd1a32faX53;from=searchresults;highlight_room=',
'BookingLink3': 'www.booking.com/hotel/us/majestic.en-gb.html?label=gen173nr-1FCAQoggJCDWNpdHlfMjAwMzMxNzNIM2IFbm9yZWZyBXVzX2lsiAEBmAEuuAEKyAEF2AEB6AEB-AELqAID;sid=28e69b52be3281ae5b7ba8b2459908ad;ucfs=1;highlighted_blocks=5670701_91458826_0_1_0;all_sr_blocks=5670701_91458826_0_1_0;room1=A%2CA;hpos=7;dest_type=city;dest_id=20033173;srfid=4a03b0b55938edff661815f856f13538dd1a32faX62;from=searchresults;highlight_room=',
'BookingLink4': 'https://www.airbnb.com/rooms/1056430',
'Hotel1': 'Private Room, Private Neighborhood, Great Location',
'Hotel2': 'Omni Chicago Hotel',
'Hotel3': 'Majestic Hotel',
'Hotel4': 'Charming space in Boystown/Lakeview',
'Price1': 62.0,
'Price2': 88.0,
'Price3': 282.0,
'Price4': 106.0,
'Route1': '#Day 1 North Avenue Beach --> Lakefront Trail --> Lincoln Park Zoo --> Maggie Daley Park   #Day 2 Shedd Aquarium --> Grant Park --> Millennium Park --> Lincoln Park',
'Route2': '#Day 1 Shedd Aquarium --> Lakefront Trail   #Day 2 Lincoln Park Zoo --> Maggie Daley Park --> North Avenue Beach --> Grant Park --> Millennium Park --> Lincoln Park',
'Route3': '#Day 1 Grant Park --> Lakefront Trail --> Lincoln Park Zoo --> Maggie Daley Park   #Day 2 Shedd Aquarium --> North Avenue Beach --> Millennium Park --> Lincoln Park',
'Route4': '#Day 1 Millennium Park --> Lakefront Trail --> Lincoln Park Zoo --> Maggie Daley Park   #Day 2 Shedd Aquarium --> North Avenue Beach --> Grant Park --> Lincoln Park'}

'''


'''	
	CHECKIN = data['checkin']
	CHECKOUT = data['checkout']
	PRICEMIN = data['pricemin']
	PRICEMAX = data['pricemax']
	AIRBNB = airbnb(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
	BOOKING = booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
	LOCATIONS = AIRBNB.append(BOOKING, ignore_index=True).iloc[:5, :]
	rv = LOCATIONS.to_dict
	context = {'checkin': rv['url'][1],
	'checkout': rv['name'][2],
	'pricemin': rv['url'][2]}
'''
