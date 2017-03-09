import googlemaps
import datetime
import pandas as pd
import csv
import re
import ast


# TRANSIT_MODE = 'driving'
# TRANSIT_MODE = 'transit'

TOMORROW = datetime.date.today() + datetime.timedelta(days=7)
T = datetime.datetime.combine(TOMORROW, datetime.time(10,0))
# General Function
def transit_time(start_index, end_index, start_df, end_df, TRANSIT_MODE):
    '''
    Get the transit time between two spots, transit_mode includs 'transit', 'driving'

    Inputs:
        start_index, end_index: integer
        transit_mode: string

    Outputs:
        transit_time: mints integer
    '''

    gmaps = googlemaps.Client(key='AIzaSyAHa_IhNh3oKBRmTDHTUvEF0EpApQwxeXw')
    start_point = start_df.loc[start_index][0]
    end_point = end_df.loc[end_index][0]
    distance_result = gmaps.distance_matrix(start_point, end_point, mode=TRANSIT_MODE, departure_time=T)
    time_element = distance_result['rows'][0]['elements'][0]['duration']['text']
    time_element = time_element.replace('s','')
    time_element = time_element.replace('min','')
    time_element = time_element.replace(' ','')
    if re.search('hour', time_element):
        time_element = time_element.replace('hour',':')
        time_element = time_element.replace(' ','')
        h,m = time_element.split(':')
        transit_time = int(h)*60 + int(m)
    else:
        transit_time = int(time_element)
    return transit_time


# depart time --> seconds integer
# input index --> refer to 'name', cord(,)


# Get between-attractions-transit-time database
# header = ['Start Point','End Point','Time(transit)','Time(driving)']
total_l = []
dic = {}
attractions = pd.read_csv('Attraction List.csv', index_col = 'Identifier')
num = int(attractions['Attraction Name'].count())
for i in range(num):
    for j in range(num):
        if i != j:
            time_transit = transit_time(i+1, j+1, attractions, attractions, 'transit')
            time_driving = transit_time(i+1, j+1, attractions, attractions, 'driving')
            dic[(i+1,j+1)] = {'time_transit': time_transit, 'time_driving': time_driving}
print (dic)


'''
        l = [[start_point, end_point, time_transit, time_driving]]
        total_l = total_l + l
my_df = pd.DataFrame(total_l)
my_df.columns = header
my_df.to_csv('attractions_transit_time.csv', index=False, header=True)
'''


'''
# For Airbnbsample, attention for cord: change string to tuple
# Sample use between two spots in airbnb
airbnb = pd.read_csv('airbnbsample.csv')
start_point = ast.literal_eval(attractions.loc[0]['cord'])
end_point = ast.literal_eval(attractions.loc[1]['cord'])
time_transit = transit_time(start_point, end_point, 'transit')
time_driving = transit_time(start_point, end_point, 'driving')
l = [[start_point, end_point, time_transit, time_driving]]
print (l)
'''


