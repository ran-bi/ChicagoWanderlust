import pandas as pd
import numpy as py
from shapely.geometry import Point
from shapely.geometry import Polygon
import json

def get_danger_polys(danger_polys_file = 'danger_poly.json'):
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

def filter_danger(locations, df):
	danger_polys = get_danger_polys(danger_polys_file = 'danger_poly.json')
	safe_locations = []
	for location in locations:
		coord = df.iloc[location][0]
		if not is_danger(coord, danger_polys):
			safe_locations.append(location)
	return safe_locations
