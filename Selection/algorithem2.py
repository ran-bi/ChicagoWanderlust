
from scrapers import airbnb, booking
import routes
import yelp_filter
import safety_filter
import final_format
import datetime

data = {'pricemax': 140, 
'attraction': ['Architecture', 'Kids/Family'], 
'checkin': datetime.date(2017, 5, 1), 
'pricemin': 50, 
'trans': 'driving', 
'checkout': datetime.date(2017, 5, 3)}

def foof(data):
    CHECKIN = data['checkin']
    CHECKOUT = data['checkout']
    PRICEMIN = data['pricemin']
    PRICEMAX = data['pricemax']
    TRANSIT_MODE = data['trans']
    PREFS = data['attraction']
    DAYS = cal_days(CHECKIN, CHECKOUT)

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

    
    find_error = None

    try:
        AIRBNB = airbnb(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
    except:
        find_error = True

    try:
        BOOKING = booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
    except:
        find_error = True

    try:
        LOCATIONS = AIRBNB.append(BOOKING, ignore_index = True)
    except:
        find_error = True

    try:
        loc_routes = routes.select_by_routes(PREFS, LOCATIONS, DAYS, TRANSIT_MODE, -1)
    except:
        cfind_error = True

    try:
        loc_lst = yelp_filter.get_filter_l(loc_routes, LOCATIONS, -1)
    except:
        find_error = True
    try:
        loc = safety_filter.filter_danger(loc_lst, LOCATIONS, loc_routes)
    except: 
        find_error = True
    
    if find_error:
        return (True, default_output)
    else:
        context = final_format.get_final_output(loc, loc_routes, routes.ATTRACTIONS, LOCATIONS)
        criteris_met = True
        return (criteris_met,context)



def cal_days(checkin, checkout):
    delta = checkout - checkin
    days = delta.days
    if days <= 2:
        return 1
    else:
        return 2


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


