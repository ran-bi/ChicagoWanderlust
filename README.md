## Chicago Wanderlust: A CS122 Project

## Synopsis

The ultimate accommodation finder for leisure travellers to Chicago.

## Code Example
```
python3 manage.py runserver
```

## Motivation



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

**Main codes are under search/util:**
-

## Troubleshooting

-**Date Input Error:** Date range must be within 10 days. Ensure check-in date is no later than check-outdate.
-**Price Range Error:** Ensure price upper bound is higher than the lower bound.
-**Webdriver Error:** The program requires installation of Chrome Webdriver in PATH.
-**Googlemaps API Error:** Googlemaps API sets limit on total daily query times. We provide a list of available API keys in search/util/APIKeys.txt. Please copy and paste a new API key to search/util/routes.py file.

## Contributors

Ran Bi,
Weijie Xin,
Leping Yu,
Minjia Zhu
@Uchicago Harris, CAPP
