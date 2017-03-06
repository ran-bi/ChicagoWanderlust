from . import booking_scraper

def foof(data):
	CHECKIN = data['checkin']
	CHECKOUT = data['checkout']
	PRICEMIN = data['pricemin']
	PRICEMAX = data['pricemax']
	AIRBNB = booking_scraper.booking(CHECKIN, CHECKOUT, PRICEMIN, PRICEMAX)
	rv = AIRBNB.iloc[:5, :].to_dict()


	criteris_met = True
	context = {'checkin': rv['url'][1],
	'checkout': rv['name'][2],
	'pricemin': rv['url'][2]}

	return (criteris_met,context)

def process(data):
	context ={'checkin': data['pricemax'],
	'checkout': data['pricemin'],
	'pricemin': data['trans']}

	return context






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