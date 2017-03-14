## Chicago Wanderlust: A CS122 Project

## Synopsis

The ultimate accommodation finder for leisure travellers to Chicago.

## Code Example
```
python3 manage.py runserver
```

## Motivation

Chicago Wanderlust is intended as a search tool for leisure travelers who are unfamiliar with the city of Chicago. It essentially provides accommodation and attraction recommendation for their stay, based on user inputs and preferences.
Being avid travelers ourselves, we understand the common challenges of planning your first trip to a popular destination. Indeed, there is more than abundant information out there on the Internet, but it takes a great amount of time to have a safe, affordable, and enjoyable journey planned out.

For example, you may need to compare locations from both hotel OTAs and Airbnb.com to find a good deal, and browse through a list of the most popular “things to do” on TripAdvisor and figure out which ones cater to your taste. Then you need to figure out where those attractions are situated, and make sure you are not staying too far away from them. After all, you want to come up with at least a tentative itinerary before you set out for your vacation. Even if you think you have taken everything into consideration, you may not have heard about the violence crimes in Chicago, and end up staying in a neighborhood not safe enough to walk around without caution.

There does not exist a single tool available in the market that can assist you in making the above decisions all at once, prompting us to fill in this blank with Chicago Wanderlust. These are the inputs we require from you: (1) check-in/check-out dates (2) price range for one night of stay (3) whether you’ll mainly rely on driving or public transit during your visit (4) Optional – your top preferences for types of attractions (up to 3).

Within a few minutes (depending on your input, and this is mainly constrained by the response time from Google Maps API), we will offer you the top 5 places to stay during your visit, each linked to the reservation page, and accompanied by a suggested 1- or 2-day itinerary (depending on your length of stay), that covers attractions tailored to your taste and tells you where to visit next. Our recommendation can be either a hotel or an Airbnb, and you can rest assured that: (1) you won’t waste much time on the road; (2) you will stay in a safe neighborhood; (3) the place has comparatively good reviews; (4) you will likely find good food around.

## Installation

**Python packages required:**
- BeautifulSoup
- Django==1.10.5
- django-bootstrap-form==3.2.1
- googlemaps
- numpy
- pandas
- rauth
- shapely
- selenium (with Chrome webdriver)

## Code Structure

**Main funcions under /search**
- /util/scrapers.py: Airbnb and Booking.com scrapers
- /util/routes.py: attraction and route selection algorithm
- /util/yelp_filter.py: restaurant quality algorithm
- /util/safety_filter.py: filter out locations in dangerous communities
- algorithm.py: consolidated function linked to front-end

**Crime data under /Preprocessing**
- csv files: raw data
- crimefilter.py: code for crimerate calculation and generate geojson file
- danger_poly.json: output geojeson file for dangerous communities

## Troubleshooting

- **Date Input Error:** Date range must be within 10 days. 
- **Webdriver Error:** The program requires installation of Chrome Webdriver in PATH.
- **Googlemaps API Error:** Googlemaps API sets limits on total daily query times. We provide a list of available API keys in search/util/APIKeys.txt. Please copy and paste a new API key to search/util/routes.py file(line 13, APIKEY) .

## Notes

- It takes around 5 minutes to run the program in VM.
- Airbnb price in our result includes reservation fee, cleaning fee, etc. The price shown on Airbnb website is room price only. 
- Airbnb price may be different from real-time price on website due to the unofficial API.

## Contributors

Ran Bi,
Weijie Xin,
Leping Yu,
Minjia Zhu
@Uchicago Harris, CAPP
