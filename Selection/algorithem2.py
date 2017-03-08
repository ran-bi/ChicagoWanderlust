
from scrapers import airbnb, booking
import routes
import yelp_filter
import safety_filter
import final_format
import datetime

data = {'pricemax': 500, 
'attraction': ['Architecture', 'Kids/Family'], 
'checkin': datetime.date(2017, 6, 1), 
'pricemin': 50, 
'trans': 'driving', 
'checkout': datetime.date(2017, 6, 3)}

def foof(data):
    CHECKIN = data['checkin']
    CHECKOUT = data['checkout']
    PRICEMIN = data['pricemin']
    PRICEMAX = data['pricemax']
    TRANSIT_MODE = data['trans']
    PREFS = data['attraction']
    DAYS = cal_days(CHECKIN, CHECKOUT)

    AIRBNB = airbnb(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
    BOOKING = booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
    LOCATIONS = AIRBNB.append(BOOKING, ignore_index = True)

    loc_routes = routes.select_by_routes(PREFS, LOCATIONS, DAYS, TRANSIT_MODE, 0)

    loc_lst = yelp_filter.get_filter_l(loc_routes, LOCATIONS, 0)
    loc = safety_filter.filter_danger(loc_lst, LOCATIONS, loc_routes)
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


