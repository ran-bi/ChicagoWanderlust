import pandas as pd
import numpy as py
from shapely.geometry import Point
from shapely.geometry import Polygon
import json

CRIMEDATA = '2016.csv'
COMM = 'CommAreas.csv'
POPULATION = 'population.csv'
BOUNDARIES = 'Boundaries.geojson'
DANGEROUSPOLYS = 'dangerous_polys.csv'
VIOLENT_CRIMES = ['ASSULT','BATTERY', 'INTIMIDATION ', 'HOMICIDE', 'OTHER OFFENSE', 'PUBLIC PEACE VIOLATION', 'ROBBERY', 'SEX OFFENSE']
PROPERTY_CRIMES = ['BURGLARY', 'THEFT', 'MOTOR VEHICLE THEFT']

def get_crimerate(crimetypes, toprate):
	raw_crimes = pd.read_csv(CRIMEDATA)
	raw_comm = pd.read_csv(COMM)
	population = pd.read_csv(POPULATION)
	pd.options.mode.chained_assignment = None

	crimes = raw_crimes[['Community Area','Beat','ID', 'Primary Type', 'Date']]
	crimes_interested = crimes[crimes['Primary Type'].isin(crimetypes)]
	crimecount = crimes_interested.groupby('Community Area')['Primary Type'].count().to_frame().reset_index()
	crimecount.columns = ['Community Area','TOTALCRIME']

	comm = raw_comm[['AREA_NUMBE', 'COMMUNITY', 'the_geom']].sort_values('AREA_NUMBE').reset_index(drop=True)
	comm_popu = pd.concat([comm, population] ,axis=1)
	crimerate = pd.concat([crimecount, comm_popu] ,axis=1).drop(['AREA_NUMBE', 'Num'],axis=1)

	crimerate['crimerate'] = crimerate['TOTALCRIME']/ crimerate['Population'] * 1000
	result = crimerate.sort_values('crimerate', ascending=False, na_position='last')
	return result.iloc[0:toprate, :]

def get_boundaries(dangercomm):
	with open(BOUNDARIES) as json_data:
		geojs = json.load(json_data)

	danger_polys = []

	for index, community in dangercomm.COMMUNITY.iteritems():
		for feature in geojs['features']:
			if feature['properties']['community'] == community:
				poly = feature['geometry']['coordinates'][0][0]
				danger_polys.append(poly)

	with open('danger_poly.json', 'w') as outfile:
		json.dump(danger_polys, outfile)

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



def check_danger(coors, danger_polys):
	point = Point(coors)
	for polygon in danger_polys:
		if polygon.contains(point):
			return True

	return False


























