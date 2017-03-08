
from scrapers import airbnb, booking
import routes
import yelp_filter
import safety_filter
import final_format



def foof(data):
	CHECKIN = data['checkin']
	CHECKOUT = data['checkout']
	PRICEMIN = data['pricemin']
	PRICEMAX = data['pricemax']
	TRANSIT_MODE = data['trans']
	PREFS = data['attraction']

	AIRBNB = airbnb(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
	BOOKING = booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
	LOCATIONS = AIRBNB.append(BOOKING, ignore_index = True)


#output from routes => loc_routes

	loc_routes = yelp_filter.get_filter_l(loc_routes, LOCATIONS, n)
	loc = safety_filter.filter_danger(loc_routes.keys(), LOCATIONS)
	context = final_format.get_final_output(loc, loc_routes, ATTRACTIONS, LOCATIONS)
	
	criteris_met = True
	return (criteris_met,context)



'''
{'pricemax': 500, 
'attraction': ['Architecture', 'Kids/Family'], 
'checkin': datetime.date(2017, 4, 1), 
'pricemin': 50, 
'trans': 'Drive', 
'checkout': datetime.date(2017, 4, 2)}
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


