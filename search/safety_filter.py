import pandas as pd
import numpy as py
from shapely.geometry import Point
from shapely.geometry import Polygon
import json
import os

output = {8: {'total travel time': 181, 'day 1 route': [(29, 1.0), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (24, 1.25), (2, 1.75), (20, 1.25)]}, \
1: {'total travel time': 167, 'day 1 route': [(17, 4.0), (8, 2.0)], 'day 2 route': [(13, 2.5), (12, 1.25), (29, 1.0), (24, 1.25), (2, 1.75), (20, 1.25)]}, \
20: {'total travel time': 223, 'day 1 route': [(24, 1.25), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (29, 1.0), (2, 1.75), (20, 1.25)]}, \
 39: {'total travel time': 179, 'day 1 route': [(2, 1.75), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (29, 1.0), (24, 1.25), (20, 1.25)]}}



def get_danger_polys(danger_polys_file = os.path.join(os.path.dirname(__file__), "danger_poly.json")):
	with open(danger_polys_file) as jsfile:
		js = json.load(jsfile)

	danger_polys = []
	for item in js:
		poly = []
		for coors in item:
			poly.append(tuple(coors))
		polygon = Polygon(poly)
		danger_polys.append(polygon)
	return danger_polys

def is_danger(coord, danger_polys):
	point = Point(coord)
	for polygon in danger_polys:
		if polygon.contains(point):
			return True
	return False

def toprank(locations, loc_routes):
	rv = []
	for i in locations:
		rv.append((loc_routes[i]['total travel time'], i))
	sort = sorted(rv)
	if len(sort) > 5:
		return [i[1] for i in sort[:5]]
	else:
		return [i[1] for i in sort]

def filter_danger(locations, df, loc_routes):
	danger_polys = get_danger_polys()
	safe_locations = []
	for location in locations:
		print(location)
		coord = df.iloc[location][0]
		if not is_danger(coord, danger_polys):
			safe_locations.append(location)
	final_result = toprank(safe_locations, loc_routes)
	return final_result





