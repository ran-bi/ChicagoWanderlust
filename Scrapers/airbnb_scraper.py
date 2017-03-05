import json
import requests
import pandas as pd


def abscraper(checkin, checkout, min_price, max_price):
	checkin = checkin.replace('-','%2D')
	checkout = checkout.replace('-', '%2D')
	url = 'https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty&checkin={}&checkout={}&locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=50&_offset=0&fetch_facets=true&guests=2&ib=false&location=Chicago%20IL%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&&price_max={}&price_min={}&sort=1'.format(checkin, checkout,max_price, min_price)
	r = requests.get(url)
	d =r.json()
	search_results = d['search_results']

	rank = 1
	all_listings = []
	
	for result in search_results:
		listing = {}
		listing['ranking'] = rank
		listing['cord'] = (float(result['listing']['lat']), float(result['listing']['lng']))
		listing['name'] = result['listing']['name']
		listing['reviews_count'] = result['listing']['reviews_count']
		listing['price'] = int(result['pricing_quote']['rate_with_service_fee']['amount'])
		listing['url'] = "https://www.airbnb.com/rooms/" + str(result['listing']['id'])

		all_listings.append(listing)
		rank += 1  

	df = pd.DataFrame(all_listings)

	return df
