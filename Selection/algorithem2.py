
from scrapers import airbnb, booking
import routes
import yelp_filter
import safety_filter
import final_format
import datetime

data = {'pricemax': 500, 
'attraction': ['Architecture', 'Kids/Family'], 
'checkin': datetime.date(2017, 4, 1), 
'pricemin': 50, 
'trans': 'Drive', 
'checkout': datetime.date(2017, 4, 2)}

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
	loc_routes = {0: {'day 1 route': [(13, 2.5), (29, 1.0), (12, 1.25), (24, 1.25), (2, 1.75)],
  'day 2 route': [(20, 1.25), (8, 2.0), (17, 4.0)],
  'total travel time': 98},
 3: {'day 1 route': [(8, 2.0), (2, 1.75), (12, 1.25), (24, 1.25)],
  'day 2 route': [(17, 4.0), (29, 1.0), (13, 2.5), (20, 1.25)],
  'total travel time': 86},
 8: {'day 1 route': [(8, 2.0), (2, 1.75), (12, 1.25), (24, 1.25)],
  'day 2 route': [(20, 1.25), (13, 2.5), (29, 1.0), (17, 4.0)],
  'total travel time': 86},
 9: {'day 1 route': [(12, 1.25), (24, 1.25), (2, 1.75), (8, 2.0), (29, 1.0)],
  'day 2 route': [(13, 2.5), (20, 1.25), (17, 4.0)],
  'total travel time': 78},
 10: {'day 1 route': [(8, 2.0), (2, 1.75), (12, 1.25), (24, 1.25)],
  'day 2 route': [(17, 4.0), (29, 1.0), (13, 2.5), (20, 1.25)],
  'total travel time': 93},
 11: {'day 1 route': [(13, 2.5), (29, 1.0), (12, 1.25), (24, 1.25), (2, 1.75)],
  'day 2 route': [(20, 1.25), (8, 2.0), (17, 4.0)],
  'total travel time': 99},
 12: {'day 1 route': [(13, 2.5), (29, 1.0), (12, 1.25), (24, 1.25), (2, 1.75)],
  'day 2 route': [(20, 1.25), (8, 2.0), (17, 4.0)],
  'total travel time': 98},
 13: {'day 1 route': [(13, 2.5), (29, 1.0), (12, 1.25), (24, 1.25), (2, 1.75)],
  'day 2 route': [(20, 1.25), (8, 2.0), (17, 4.0)],
  'total travel time': 96},
 15: {'day 1 route': [(20, 1.25),
   (13, 2.5),
   (29, 1.0),
   (12, 1.25),
   (24, 1.25)],
  'day 2 route': [(2, 1.75), (8, 2.0), (17, 4.0)],
  'total travel time': 96},
 16: {'day 1 route': [(8, 2.0), (2, 1.75), (12, 1.25), (24, 1.25)],
  'day 2 route': [(17, 4.0), (29, 1.0), (13, 2.5), (20, 1.25)],
  'total travel time': 81},
 17: {'day 1 route': [(8, 2.0), (2, 1.75), (12, 1.25), (24, 1.25)],
  'day 2 route': [(17, 4.0), (29, 1.0), (13, 2.5), (20, 1.25)],
  'total travel time': 98},
 19: {'day 1 route': [(12, 1.25), (24, 1.25), (2, 1.75), (8, 2.0), (29, 1.0)],
  'day 2 route': [(13, 2.5), (20, 1.25), (17, 4.0)],
  'total travel time': 75}}

	loc_lst = yelp_filter.get_filter_l(loc_routes, LOCATIONS, 0)
	loc = safety_filter.filter_danger(loc_lst, LOCATIONS, loc_routes)
	context = final_format.get_final_output(loc, loc_routes, routes.ATTRACTIONS, LOCATIONS)
	
	criteris_met = True
	return (criteris_met,loc)








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


