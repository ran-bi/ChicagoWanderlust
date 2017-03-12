import pandas as pd
import numpy as py
from shapely.geometry import Point
from shapely.geometry import Polygon
import json
import os

def get_danger_polys(danger_polys_file = os.path.join(os.path.dirname(__file__), "danger_poly.json")):
	'''
	Take geojson file, return a list of Polygon objects.

	Input:
		danger_polys_file: path of the geojson file containing multipolygon coordinates of each dangerous community.

	Output:
		danger_polys: a list of Polygon objects, each Polygon represents the boundary of a dangerous community.
	'''
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
	'''
	Check whether a given location falls in dangerous community.

	Inputs:
		coord: tuple of floats, representing geographic coordinates.
		danger_polys: list of Polygon objects.
	Output:
		bool: True if the location falls in dangerous community.
	'''
	point = Point(coord)
	for polygon in danger_polys:
		if polygon.contains(point):
			return True
	return False

def toprank(locations, loc_routes):
	'''
	Rank the list of locations by travel time and return the top five results.

	Input:
		location: list of location index.
		loc_routes: a dictionary. key - index of location
        value: dictionary {"day 1 route" or "route": list of tuples,
        (if applicable) "day 2 route": list of tuples,
        "total travel time": int}

    Output:
    	list of location index.
	'''

	rv = []
	for i in locations:
		rv.append((loc_routes[i]['total travel time'], i))
	sort = sorted(rv)
	if len(sort) > 5:
		return [i[1] for i in sort[:5]]
	else:
		return [i[1] for i in sort]

def filter_danger(locations, df, loc_routes):
	'''
	Filter out locations that fall in dangerous communities. Return the top five locations with shortest travel time.

	Input:
		location: list of location index.
		df: LOCATIONS dataframe
		loc_routes: a dictionary. key - index of location
        value: dictionary {"day 1 route" or "route": list of tuples,
        (if applicable) "day 2 route": list of tuples,
        "total travel time": int}

    Output:
    	list of location index.
	'''
	danger_polys = get_danger_polys()
	safe_locations = []
	for location in locations:
		print(location)
		coord = df.iloc[location][0]
		if not is_danger(coord, danger_polys):
			safe_locations.append(location)
	final_result = toprank(safe_locations, loc_routes)
	return final_result





