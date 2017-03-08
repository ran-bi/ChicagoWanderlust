import re
import json
import requests
from datetime import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def airbnb(checkin, checkout, min_price, max_price, toprate=15):
	checkin = checkin.strftime('%Y-%m-%d')
	checkin = checkin.replace('-','%2D')
	checkout = checkout.strftime('%Y-%m-%d')
	checkout = checkout.replace('-', '%2D')
	url = 'https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty&checkin={}&checkout={}&locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=50&_offset=0&fetch_facets=true&guests=2&ib=false&location=Chicago%20IL%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&&price_max={}&price_min={}&sort=1'.format(checkin, checkout,max_price, min_price)
	r = requests.get(url)
	d =r.json()
	search_results = d['search_results']

	rank = 1
	all_listings = []
	
	for result in search_results:
		listing = {}
#		listing['ranking'] = rank
		listing['coord'] = (float(result['listing']['lat']), float(result['listing']['lng']))
		listing['name'] = result['listing']['name']
#		listing['reviews_count'] = result['listing']['reviews_count']
		listing['price'] = int(result['pricing_quote']['rate_with_service_fee']['amount'])
		listing['url'] = "https://www.airbnb.com/rooms/" + str(result['listing']['id'])

		all_listings.append(listing)
		rank += 1  

	df = pd.DataFrame(all_listings)

	return df.iloc[:toprate, :]

def booking(checkin, checkout, minprice, maxprice, toprate=15):

	checkin_monthday = checkin.strftime('%d')
	checkin_year_month = checkin.strftime('%Y-%m')
	checkout_monthday = checkout.strftime('%d')
	checkout_year_month = checkout.strftime('%Y-%m')
	delta = checkout - checkin

	url = "http://www.booking.com/searchresults.html"
	payload = {
	'si':'ai,co,ci,re,di',
	'dest_type':'city',
	'dest_id':'20033173',
	'checkin_monthday': checkin_monthday,
	'checkin_year_month': checkin_year_month,
	'checkout_monthday':checkout_monthday,
	'checkout_year_month':checkout_year_month,
	'sb_travel_purpose':'leisure',
	'src':'index',
	'nflt':'',
	'ss_raw':'',
	'dcid':'4'
	}
	head = {"User-Agent":"Safari/537.36"}


	hotels = []
	page_count = 1

	driver = webdriver.Chrome()
	driver.set_page_load_timeout(30)


	r = requests.post(url, payload, headers=head)
	searchlink = r.url
	nextpage = True


	while page_count < 5 and nextpage:
		driver.get(searchlink)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		tables = soup.find_all("div", class_=re.compile('sr_item_content'))
		for table in tables:
			raw_url = table.a.get('href')
			raw_name = table.find('span', {'class': 'sr-hotel__name'})
#			raw_rating = table.find("span", {"class" : "average"})
#			raw_review = table.find('span', {'class': 'score_from_number_of_reviews'})
			raw_price = table.find('strong', class_=re.compile('price scarcity_color'))
			raw_coord = table.find_all('a')[1]

			hotel = {}
			hotel['url'] = 'www.booking.com' + raw_url if raw_url else None
			hotel['name'] = raw_name.text.strip() if raw_name else None
#			hotel['rating'] = float(raw_rating.text.strip()) if raw_rating else None
#			hotel['review'] = raw_review.text.strip().split()[0] if raw_review else None
			hotel['price'] = float(raw_price.find('b').text.strip()[3:].replace(",", "")) / delta.days if raw_price else None
			coord = tuple([float(i) for i in raw_coord.get('data-coords').split(",")]) if raw_coord else None
			hotel['coord'] = (coord[1], coord[0]) if coord else None
			hotels.append(hotel)
			print(hotel['name'])

		raw_nextpage = soup.select('a[class*=paging-next]')
		nextpage = 'http://www.booking.com' + raw_nextpage[0].get('href') if raw_nextpage else None
		print(nextpage)
		page_count += 1
		searchlink = nextpage if nextpage else None

	driver.close()

	df = pd.DataFrame(hotels)
	selected = df[df.price.between(minprice, maxprice, inclusive = True)]
	if len(selected) < toprate:
		return selected
	else:
		return selected.iloc[:toprate,:]


