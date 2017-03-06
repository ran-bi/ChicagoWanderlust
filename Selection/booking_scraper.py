import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import numpy as np
from datetime import datetime


def booking(checkin, checkout, minprice, maxprice):
	checkin_monthday = checkin[-2:]
	checkin_year_month = checkin[:-3]
	checkout_monthday = checkout[-2:]
	checkout_year_month = checkout[:-3]

	date_format = "%Y-%m-%d"
	checkindate = datetime.strptime(checkin, date_format)
	checkoutdate = datetime.strptime(checkout, date_format)
	delta = checkoutdate - checkindate

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
	driver.set_page_load_timeout(10)


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
			raw_rating = table.find("span", {"class" : "average"})
			raw_review = table.find('span', {'class': 'score_from_number_of_reviews'})
			raw_price = table.find('strong', class_=re.compile('price scarcity_color'))
			raw_coord = table.find_all('a')[1]

			hotel = {}
			hotel['url'] = 'www.booking.com' + raw_url if raw_url else None
			hotel['name'] = raw_name.text.strip() if raw_name else None
#			hotel['rating'] = float(raw_rating.text.strip()) if raw_rating else None
#			hotel['review'] = raw_review.text.strip().split()[0] if raw_review else None
			hotel['price'] = float(raw_price.find('b').text.strip()[3:].replace(",", "")) / delta.days if raw_price else None
			hotel['coord'] = tuple([float(i) for i in raw_coord.get('data-coords').split(",")]) if raw_coord else None
			hotels.append(hotel)
#			print(hotel['name'])

		raw_nextpage = soup.select('a[class*=paging-next]')
		nextpage = 'http://www.booking.com' + raw_nextpage[0].get('href') if raw_nextpage else None
#		print(nextpage)
		page_count += 1
		searchlink = nextpage if nextpage else None

	driver.close()

	df = pd.DataFrame(hotels)
	selected = df[df.price.between(minprice, maxprice, inclusive = True)]


	return selected







