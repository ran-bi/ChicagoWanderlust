import pandas as pd
import numpy as np
import random
import googlemaps
import datetime
import statistics
import csv
import re
import ast
import os
from .scrapers import airbnb, booking

'''
AIRBNB = airbnb(datetime.datetime(2017,4,20), datetime.datetime(2017,4,22), 50, 400)
BOOKING = booking(datetime.datetime(2017,4,20), datetime.datetime(2017,4,22), 50, 400)
LOCATIONS = AIRBNB.append(BOOKING, ignore_index = True)
'''

TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
T = datetime.datetime.combine(TOMORROW, datetime.time(10,0))
#ATTRACTIONS = pd.read_csv('Attraction List.csv', index_col = 'Identifier')
ATTRACTIONS = pd.read_csv(os.path.join(os.path.dirname(__file__), "Attraction List.csv"), index_col = 'Identifier')
STORED = {(7, 3): {'time_driving': 8, 'time_transit': 16}, (31, 6): {'time_driving': 17, 'time_transit': 25}, (5, 31): {'time_driving': 13, 'time_transit': 38}, (20, 25): {'time_driving': 17, 'time_transit': 23}, (16, 9): {'time_driving': 25, 'time_transit': 47}, (6, 28): {'time_driving': 4, 'time_transit': 5}, (21, 28): {'time_driving': 13, 'time_transit': 16}, (19, 4): {'time_driving': 29, 'time_transit': 54}, (17, 20): {'time_driving': 18, 'time_transit': 35}, (7, 25): {'time_driving': 12, 'time_transit': 22}, (22, 19): {'time_driving': 18, 'time_transit': 53}, (20, 7): {'time_driving': 20, 'time_transit': 37}, (30, 26): {'time_driving': 19, 'time_transit': 45}, (18, 19): {'time_driving': 18, 'time_transit': 58}, (23, 26): {'time_driving': 1, 'time_transit': 4}, (21, 6): {'time_driving': 13, 'time_transit': 16}, (8, 5): {'time_driving': 11, 'time_transit': 28}, (32, 2): {'time_driving': 18, 'time_transit': 46}, (13, 32): {'time_driving': 22, 'time_transit': 73}, (14, 31): {'time_driving': 13, 'time_transit': 27}, (10, 7): {'time_driving': 13, 'time_transit': 32}, (15, 30): {'time_driving': 17, 'time_transit': 29}, (11, 22): {'time_driving': 9, 'time_transit': 18}, (24, 14): {'time_driving': 3, 'time_transit': 10}, (14, 1): {'time_driving': 4, 'time_transit': 11}, (12, 17): {'time_driving': 11, 'time_transit': 19}, (1, 28): {'time_driving': 7, 'time_transit': 12}, (25, 15): {'time_driving': 2, 'time_transit': 5}, (15, 4): {'time_driving': 18, 'time_transit': 19}, (13, 20): {'time_driving': 6, 'time_transit': 9}, (2, 27): {'time_driving': 10, 'time_transit': 25}, (26, 12): {'time_driving': 5, 'time_transit': 20}, (29, 17): {'time_driving': 16, 'time_transit': 53}, (3, 2): {'time_driving': 1, 'time_transit': 2}, (27, 1): {'time_driving': 10, 'time_transit': 21}, (30, 14): {'time_driving': 14, 'time_transit': 30}, (4, 5): {'time_driving': 25, 'time_transit': 53}, (28, 10): {'time_driving': 4, 'time_transit': 8}, (31, 15): {'time_driving': 16, 'time_transit': 15}, (5, 24): {'time_driving': 14, 'time_transit': 31}, (20, 32): {'time_driving': 26, 'time_transit': 55}, (6, 23): {'time_driving': 10, 'time_transit': 18}, (30, 16): {'time_driving': 22, 'time_transit': 62}, (19, 13): {'time_driving': 21, 'time_transit': 57}, (17, 13): {'time_driving': 11, 'time_transit': 40}, (7, 22): {'time_driving': 11, 'time_transit': 36}, (31, 21): {'time_driving': 13, 'time_transit': 17}, (20, 14): {'time_driving': 15, 'time_transit': 26}, (18, 10): {'time_driving': 16, 'time_transit': 38}, (23, 19): {'time_driving': 18, 'time_transit': 61}, (21, 15): {'time_driving': 7, 'time_transit': 10}, (8, 12): {'time_driving': 3, 'time_transit': 16}, (32, 25): {'time_driving': 21, 'time_transit': 40}, (22, 12): {'time_driving': 6, 'time_transit': 26}, (23, 9): {'time_driving': 11, 'time_transit': 36}, (10, 14): {'time_driving': 7, 'time_transit': 11}, (8, 18): {'time_driving': 13, 'time_transit': 40}, (11, 15): {'time_driving': 2, 'time_transit': 2}, (9, 19): {'time_driving': 18, 'time_transit': 42}, (24, 21): {'time_driving': 9, 'time_transit': 17}, (14, 8): {'time_driving': 5, 'time_transit': 22}, (12, 8): {'time_driving': 4, 'time_transit': 17}, (1, 21): {'time_driving': 7, 'time_transit': 7}, (25, 16): {'time_driving': 20, 'time_transit': 35}, (15, 13): {'time_driving': 10, 'time_transit': 19}, (2, 18): {'time_driving': 10, 'time_transit': 27}, (26, 23): {'time_driving': 1, 'time_transit': 4}, (3, 11): {'time_driving': 2, 'time_transit': 3}, (27, 6): {'time_driving': 15, 'time_transit': 34}, (1, 15): {'time_driving': 5, 'time_transit': 5}, (4, 12): {'time_driving': 14, 'time_transit': 29}, (28, 1): {'time_driving': 6, 'time_transit': 15}, (2, 12): {'time_driving': 1, 'time_transit': 7}, (5, 1): {'time_driving': 14, 'time_transit': 29}, (29, 4): {'time_driving': 11, 'time_transit': 27}, (3, 17): {'time_driving': 12, 'time_transit': 17}, (16, 7): {'time_driving': 16, 'time_transit': 34}, (6, 14): {'time_driving': 9, 'time_transit': 13}, (30, 27): {'time_driving': 18, 'time_transit': 37}, (19, 18): {'time_driving': 22, 'time_transit': 61}, (17, 6): {'time_driving': 12, 'time_transit': 35}, (7, 15): {'time_driving': 10, 'time_transit': 21}, (31, 18): {'time_driving': 15, 'time_transit': 38}, (20, 21): {'time_driving': 17, 'time_transit': 22}, (18, 5): {'time_driving': 17, 'time_transit': 60}, (16, 29): {'time_driving': 22, 'time_transit': 66}, (6, 32): {'time_driving': 23, 'time_transit': 53}, (21, 8): {'time_driving': 7, 'time_transit': 18}, (17, 24): {'time_driving': 8, 'time_transit': 22}, (32, 16): {'time_driving': 6, 'time_transit': 12}, (22, 7): {'time_driving': 12, 'time_transit': 35}, (18, 31): {'time_driving': 13, 'time_transit': 49}, (23, 6): {'time_driving': 8, 'time_transit': 20}, (10, 9): {'time_driving': 13, 'time_transit': 23}, (8, 25): {'time_driving': 8, 'time_transit': 20}, (11, 4): {'time_driving': 16, 'time_transit': 22}, (9, 20): {'time_driving': 16, 'time_transit': 23}, (24, 28): {'time_driving': 5, 'time_transit': 17}, (14, 19): {'time_driving': 15, 'time_transit': 36}, (12, 7): {'time_driving': 8, 'time_transit': 18}, (10, 19): {'time_driving': 20, 'time_transit': 38}, (15, 10): {'time_driving': 6, 'time_transit': 10}, (13, 6): {'time_driving': 6, 'time_transit': 13}, (11, 26): {'time_driving': 6, 'time_transit': 12}, (26, 30): {'time_driving': 18, 'time_transit': 52}, (24, 2): {'time_driving': 3, 'time_transit': 6}, (12, 29): {'time_driving': 6, 'time_transit': 27}, (27, 31): {'time_driving': 14, 'time_transit': 30}, (25, 3): {'time_driving': 5, 'time_transit': 8}, (4, 11): {'time_driving': 15, 'time_transit': 22}, (28, 24): {'time_driving': 5, 'time_transit': 17}, (2, 7): {'time_driving': 7, 'time_transit': 14}, (5, 10): {'time_driving': 18, 'time_transit': 42}, (3, 22): {'time_driving': 9, 'time_transit': 22}, (6, 1): {'time_driving': 9, 'time_transit': 17}, (30, 2): {'time_driving': 14, 'time_transit': 27}, (4, 17): {'time_driving': 23, 'time_transit': 38}, (19, 27): {'time_driving': 16, 'time_transit': 47}, (7, 4): {'time_driving': 18, 'time_transit': 37}, (31, 27): {'time_driving': 12, 'time_transit': 29}, (5, 20): {'time_driving': 25, 'time_transit': 52}, (20, 28): {'time_driving': 13, 'time_transit': 22}, (16, 20): {'time_driving': 30, 'time_transit': 56}, (6, 27): {'time_driving': 16, 'time_transit': 35}, (21, 17): {'time_driving': 13, 'time_transit': 23}, (19, 1): {'time_driving': 16, 'time_transit': 38}, (32, 23): {'time_driving': 20, 'time_transit': 56}, (22, 30): {'time_driving': 20, 'time_transit': 43}, (18, 22): {'time_driving': 18, 'time_transit': 42}, (23, 31): {'time_driving': 16, 'time_transit': 43}, (12, 32): {'time_driving': 18, 'time_transit': 53}, (32, 13): {'time_driving': 22, 'time_transit': 56}, (9, 29): {'time_driving': 12, 'time_transit': 32}, (14, 26): {'time_driving': 6, 'time_transit': 12}, (10, 26): {'time_driving': 10, 'time_transit': 18}, (15, 19): {'time_driving': 18, 'time_transit': 32}, (11, 19): {'time_driving': 16, 'time_transit': 29}, (26, 25): {'time_driving': 10, 'time_transit': 19}, (24, 9): {'time_driving': 9, 'time_transit': 20}, (12, 20): {'time_driving': 13, 'time_transit': 27}, (27, 20): {'time_driving': 21, 'time_transit': 38}, (1, 25): {'time_driving': 6, 'time_transit': 7}, (25, 4): {'time_driving': 18, 'time_transit': 22}, (13, 25): {'time_driving': 11, 'time_transit': 21}, (28, 23): {'time_driving': 8, 'time_transit': 14}, (2, 30): {'time_driving': 17, 'time_transit': 32}, (26, 3): {'time_driving': 7, 'time_transit': 24}, (29, 22): {'time_driving': 3, 'time_transit': 9}, (3, 31): {'time_driving': 14, 'time_transit': 21}, (27, 10): {'time_driving': 15, 'time_transit': 33}, (30, 5): {'time_driving': 18, 'time_transit': 62}, (4, 24): {'time_driving': 14, 'time_transit': 29}, (19, 32): {'time_driving': 3, 'time_transit': 7}, (5, 29): {'time_driving': 17, 'time_transit': 57}, (20, 27): {'time_driving': 23, 'time_transit': 38}, (27, 32): {'time_driving': 20, 'time_transit': 43}, (16, 11): {'time_driving': 20, 'time_transit': 37}, (6, 18): {'time_driving': 19, 'time_transit': 40}, (21, 26): {'time_driving': 12, 'time_transit': 23}, (19, 6): {'time_driving': 21, 'time_transit': 46}, (18, 32): {'time_driving': 18, 'time_transit': 58}, (17, 10): {'time_driving': 12, 'time_transit': 24}, (7, 27): {'time_driving': 4, 'time_transit': 8}, (22, 17): {'time_driving': 15, 'time_transit': 35}, (20, 1): {'time_driving': 15, 'time_transit': 26}, (18, 17): {'time_driving': 18, 'time_transit': 43}, (23, 20): {'time_driving': 15, 'time_transit': 36}, (21, 4): {'time_driving': 22, 'time_transit': 28}, (8, 7): {'time_driving': 7, 'time_transit': 15}, (32, 4): {'time_driving': 30, 'time_transit': 53}, (22, 11): {'time_driving': 7, 'time_transit': 20}, (9, 6): {'time_driving': 14, 'time_transit': 22}, (14, 29): {'time_driving': 7, 'time_transit': 21}, (10, 5): {'time_driving': 19, 'time_transit': 39}, (15, 24): {'time_driving': 4, 'time_transit': 9}, (11, 8): {'time_driving': 6, 'time_transit': 16}, (24, 16): {'time_driving': 16, 'time_transit': 35}, (14, 7): {'time_driving': 10, 'time_transit': 27}, (12, 19): {'time_driving': 14, 'time_transit': 35}, (1, 18): {'time_driving': 16, 'time_transit': 28}, (25, 13): {'time_driving': 10, 'time_transit': 20}, (15, 6): {'time_driving': 8, 'time_transit': 12}, (13, 18): {'time_driving': 19, 'time_transit': 40}, (2, 25): {'time_driving': 6, 'time_transit': 7}, (26, 10): {'time_driving': 8, 'time_transit': 15}, (23, 32): {'time_driving': 23, 'time_transit': 61}, (3, 4): {'time_driving': 16, 'time_transit': 27}, (27, 3): {'time_driving': 12, 'time_transit': 24}, (30, 12): {'time_driving': 13, 'time_transit': 31}, (4, 7): {'time_driving': 20, 'time_transit': 38}, (28, 4): {'time_driving': 15, 'time_transit': 23}, (31, 9): {'time_driving': 13, 'time_transit': 21}, (5, 6): {'time_driving': 18, 'time_transit': 42}, (29, 9): {'time_driving': 13, 'time_transit': 35}, (16, 2): {'time_driving': 19, 'time_transit': 35}, (6, 21): {'time_driving': 14, 'time_transit': 24}, (30, 22): {'time_driving': 20, 'time_transit': 43}, (19, 15): {'time_driving': 20, 'time_transit': 36}, (17, 3): {'time_driving': 9, 'time_transit': 16}, (7, 16): {'time_driving': 15, 'time_transit': 28}, (31, 23): {'time_driving': 15, 'time_transit': 39}, (5, 32): {'time_driving': 7, 'time_transit': 15}, (20, 8): {'time_driving': 16, 'time_transit': 38}, (18, 8): {'time_driving': 12, 'time_transit': 38}, (16, 24): {'time_driving': 19, 'time_transit': 44}, (21, 13): {'time_driving': 14, 'time_transit': 21}, (8, 14): {'time_driving': 4, 'time_transit': 17}, (32, 27): {'time_driving': 17, 'time_transit': 44}, (22, 2): {'time_driving': 7, 'time_transit': 21}, (9, 15): {'time_driving': 8, 'time_transit': 10}, (23, 11): {'time_driving': 7, 'time_transit': 22}, (10, 12): {'time_driving': 6, 'time_transit': 16}, (8, 20): {'time_driving': 14, 'time_transit': 37}, (11, 1): {'time_driving': 2, 'time_transit': 5}, (9, 17): {'time_driving': 14, 'time_transit': 27}, (24, 23): {'time_driving': 5, 'time_transit': 16}, (12, 10): {'time_driving': 6, 'time_transit': 17}, (10, 22): {'time_driving': 9, 'time_transit': 14}, (25, 22): {'time_driving': 12, 'time_transit': 18}, (13, 11): {'time_driving': 7, 'time_transit': 24}, (2, 16): {'time_driving': 17, 'time_transit': 31}, (26, 21): {'time_driving': 12, 'time_transit': 26}, (3, 13): {'time_driving': 8, 'time_transit': 25}, (27, 24): {'time_driving': 11, 'time_transit': 31}, (1, 13): {'time_driving': 8, 'time_transit': 26}, (4, 14): {'time_driving': 15, 'time_transit': 28}, (28, 3): {'time_driving': 8, 'time_transit': 14}, (2, 10): {'time_driving': 5, 'time_transit': 12}, (5, 15): {'time_driving': 17, 'time_transit': 29}, (29, 2): {'time_driving': 8, 'time_transit': 24}, (3, 19): {'time_driving': 16, 'time_transit': 33}, (6, 12): {'time_driving': 8, 'time_transit': 19}, (30, 25): {'time_driving': 15, 'time_transit': 25}, (4, 20): {'time_driving': 12, 'time_transit': 14}, (19, 20): {'time_driving': 28, 'time_transit': 52}, (17, 4): {'time_driving': 19, 'time_transit': 37}, (7, 9): {'time_driving': 13, 'time_transit': 22}, (31, 28): {'time_driving': 15, 'time_transit': 25}, (20, 23): {'time_driving': 17, 'time_transit': 35}, (18, 3): {'time_driving': 13, 'time_transit': 28}, (16, 31): {'time_driving': 17, 'time_transit': 38}, (21, 22): {'time_driving': 14, 'time_transit': 19}, (17, 30): {'time_driving': 16, 'time_transit': 38}, (32, 18): {'time_driving': 21, 'time_transit': 58}, (22, 5): {'time_driving': 17, 'time_transit': 49}, (11, 32): {'time_driving': 20, 'time_transit': 46}, (18, 29): {'time_driving': 15, 'time_transit': 51}, (8, 27): {'time_driving': 10, 'time_transit': 23}, (32, 8): {'time_driving': 15, 'time_transit': 55}, (11, 6): {'time_driving': 7, 'time_transit': 13}, (9, 26): {'time_driving': 13, 'time_transit': 28}, (24, 30): {'time_driving': 17, 'time_transit': 36}, (14, 17): {'time_driving': 13, 'time_transit': 21}, (12, 1): {'time_driving': 3, 'time_transit': 8}, (10, 17): {'time_driving': 16, 'time_transit': 34}, (25, 31): {'time_driving': 15, 'time_transit': 19}, (15, 20): {'time_driving': 17, 'time_transit': 17}, (13, 4): {'time_driving': 11, 'time_transit': 14}, (28, 32): {'time_driving': 21, 'time_transit': 61}, (11, 28): {'time_driving': 8, 'time_transit': 11}, (26, 28): {'time_driving': 6, 'time_transit': 13}, (24, 4): {'time_driving': 14, 'time_transit': 29}, (12, 31): {'time_driving': 12, 'time_transit': 25}, (27, 17): {'time_driving': 3, 'time_transit': 6}, (1, 6): {'time_driving': 9, 'time_transit': 14}, (25, 1): {'time_driving': 4, 'time_transit': 9}, (13, 30): {'time_driving': 20, 'time_transit': 50}, (28, 26): {'time_driving': 7, 'time_transit': 13}, (2, 5): {'time_driving': 13, 'time_transit': 22}, (26, 6): {'time_driving': 7, 'time_transit': 18}, (5, 8): {'time_driving': 11, 'time_transit': 33}, (29, 27): {'time_driving': 15, 'time_transit': 51}, (3, 24): {'time_driving': 2, 'time_transit': 8}, (6, 7): {'time_driving': 14, 'time_transit': 34}, (4, 19): {'time_driving': 26, 'time_transit': 53}, (19, 29): {'time_driving': 20, 'time_transit': 65}, (26, 32): {'time_driving': 22, 'time_transit': 59}, (7, 6): {'time_driving': 11, 'time_transit': 33}, (31, 5): {'time_driving': 13, 'time_transit': 39}, (5, 18): {'time_driving': 23, 'time_transit': 56}, (20, 30): {'time_driving': 23, 'time_transit': 42}, (16, 22): {'time_driving': 24, 'time_transit': 58}, (6, 25): {'time_driving': 11, 'time_transit': 17}, (21, 31): {'time_driving': 12, 'time_transit': 18}, (19, 3): {'time_driving': 18, 'time_transit': 40}, (17, 23): {'time_driving': 10, 'time_transit': 35}, (7, 28): {'time_driving': 9, 'time_transit': 23}, (22, 28): {'time_driving': 5, 'time_transit': 13}, (20, 4): {'time_driving': 13, 'time_transit': 14}, (18, 20): {'time_driving': 17, 'time_transit': 40}, (23, 25): {'time_driving': 11, 'time_transit': 21}, (8, 2): {'time_driving': 3, 'time_transit': 11}, (32, 15): {'time_driving': 21, 'time_transit': 36}, (9, 3): {'time_driving': 8, 'time_transit': 15}, (14, 24): {'time_driving': 3, 'time_transit': 8}, (10, 24): {'time_driving': 6, 'time_transit': 16}, (15, 29): {'time_driving': 9, 'time_transit': 26}, (11, 21): {'time_driving': 6, 'time_transit': 10}, (24, 11): {'time_driving': 3, 'time_transit': 7}, (14, 2): {'time_driving': 3, 'time_transit': 8}, (12, 22): {'time_driving': 7, 'time_transit': 24}, (27, 22): {'time_driving': 15, 'time_transit': 44}, (1, 31): {'time_driving': 12, 'time_transit': 18}, (25, 10): {'time_driving': 7, 'time_transit': 11}, (13, 23): {'time_driving': 8, 'time_transit': 34}, (28, 17): {'time_driving': 14, 'time_transit': 32}, (2, 28): {'time_driving': 6, 'time_transit': 12}, (26, 1): {'time_driving': 6, 'time_transit': 25}, (29, 20): {'time_driving': 10, 'time_transit': 22}, (3, 1): {'time_driving': 3, 'time_transit': 3}, (27, 12): {'time_driving': 11, 'time_transit': 31}, (30, 11): {'time_driving': 14, 'time_transit': 24}, (4, 26): {'time_driving': 15, 'time_transit': 35}, (28, 15): {'time_driving': 8, 'time_transit': 11}, (31, 2): {'time_driving': 13, 'time_transit': 19}, (5, 27): {'time_driving': 13, 'time_transit': 33}, (29, 14): {'time_driving': 8, 'time_transit': 24}, (16, 13): {'time_driving': 23, 'time_transit': 61}, (6, 16): {'time_driving': 22, 'time_transit': 49}, (21, 24): {'time_driving': 8, 'time_transit': 14}, (4, 32): {'time_driving': 30, 'time_transit': 56}, (19, 8): {'time_driving': 14, 'time_transit': 42}, (17, 8): {'time_driving': 5, 'time_transit': 13}, (7, 21): {'time_driving': 11, 'time_transit': 22}, (22, 23): {'time_driving': 8, 'time_transit': 29}, (20, 3): {'time_driving': 17, 'time_transit': 25}, (18, 15): {'time_driving': 15, 'time_transit': 25}, (23, 22): {'time_driving': 8, 'time_transit': 29}, (21, 2): {'time_driving': 6, 'time_transit': 8}, (8, 9): {'time_driving': 9, 'time_transit': 23}, (32, 6): {'time_driving': 22, 'time_transit': 45}, (22, 9): {'time_driving': 12, 'time_transit': 24}, (9, 4): {'time_driving': 22, 'time_transit': 32}, (23, 12): {'time_driving': 6, 'time_transit': 23}, (10, 3): {'time_driving': 8, 'time_transit': 14}, (15, 26): {'time_driving': 8, 'time_transit': 12}, (11, 10): {'time_driving': 7, 'time_transit': 11}, (24, 18): {'time_driving': 12, 'time_transit': 34}, (14, 5): {'time_driving': 15, 'time_transit': 28}, (12, 13): {'time_driving': 6, 'time_transit': 27}, (1, 16): {'time_driving': 17, 'time_transit': 30}, (25, 19): {'time_driving': 18, 'time_transit': 36}, (13, 16): {'time_driving': 20, 'time_transit': 61}, (2, 23): {'time_driving': 6, 'time_transit': 16}, (26, 8): {'time_driving': 7, 'time_transit': 27}, (3, 6): {'time_driving': 7, 'time_transit': 14}, (27, 5): {'time_driving': 15, 'time_transit': 30}, (1, 10): {'time_driving': 8, 'time_transit': 13}, (4, 1): {'time_driving': 15, 'time_transit': 25}, (28, 6): {'time_driving': 3, 'time_transit': 5}, (31, 11): {'time_driving': 14, 'time_transit': 18}, (5, 4): {'time_driving': 26, 'time_transit': 58}, (29, 7): {'time_driving': 13, 'time_transit': 50}, (16, 4): {'time_driving': 31, 'time_transit': 58}, (6, 11): {'time_driving': 8, 'time_transit': 13}, (30, 20): {'time_driving': 21, 'time_transit': 45}, (19, 17): {'time_driving': 17, 'time_transit': 37}, (17, 1): {'time_driving': 7, 'time_transit': 14}, (7, 18): {'time_driving': 16, 'time_transit': 45}, (31, 17): {'time_driving': 13, 'time_transit': 25}, (20, 10): {'time_driving': 17, 'time_transit': 19}, (18, 6): {'time_driving': 15, 'time_transit': 43}, (16, 26): {'time_driving': 20, 'time_transit': 59}, (21, 11): {'time_driving': 6, 'time_transit': 9}, (10, 32): {'time_driving': 23, 'time_transit': 41}, (17, 27): {'time_driving': 4, 'time_transit': 9}, (32, 29): {'time_driving': 21, 'time_transit': 62}, (29, 32): {'time_driving': 22, 'time_transit': 72}, (9, 13): {'time_driving': 16, 'time_transit': 23}, (23, 5): {'time_driving': 17, 'time_transit': 60}, (8, 22): {'time_driving': 7, 'time_transit': 37}, (11, 3): {'time_driving': 3, 'time_transit': 3}, (9, 23): {'time_driving': 14, 'time_transit': 30}, (24, 25): {'time_driving': 7, 'time_transit': 14}, (14, 12): {'time_driving': 3, 'time_transit': 8}, (12, 4): {'time_driving': 14, 'time_transit': 29}, (10, 20): {'time_driving': 15, 'time_transit': 18}, (25, 20): {'time_driving': 17, 'time_transit': 20}, (15, 9): {'time_driving': 7, 'time_transit': 10}, (13, 9): {'time_driving': 12, 'time_transit': 28}, (11, 25): {'time_driving': 4, 'time_transit': 5}, (26, 19): {'time_driving': 17, 'time_transit': 58}, (3, 15): {'time_driving': 3, 'time_transit': 9}, (27, 26): {'time_driving': 12, 'time_transit': 45}, (1, 3): {'time_driving': 1, 'time_transit': 3}, (4, 8): {'time_driving': 16, 'time_transit': 37}, (28, 29): {'time_driving': 6, 'time_transit': 14}, (2, 8): {'time_driving': 5, 'time_transit': 11}, (5, 13): {'time_driving': 18, 'time_transit': 57}, (3, 21): {'time_driving': 7, 'time_transit': 12}, (25, 32): {'time_driving': 19, 'time_transit': 39}, (6, 2): {'time_driving': 8, 'time_transit': 14}, (30, 31): {'time_driving': 12, 'time_transit': 23}, (4, 22): {'time_driving': 11, 'time_transit': 20}, (19, 22): {'time_driving': 21, 'time_transit': 52}, (7, 11): {'time_driving': 8, 'time_transit': 16}, (31, 30): {'time_driving': 12, 'time_transit': 24}, (5, 23): {'time_driving': 16, 'time_transit': 46}, (20, 17): {'time_driving': 23, 'time_transit': 37}, (18, 1): {'time_driving': 11, 'time_transit': 26}, (16, 17): {'time_driving': 19, 'time_transit': 35}, (21, 20): {'time_driving': 16, 'time_transit': 23}, (17, 28): {'time_driving': 10, 'time_transit': 24}, (32, 20): {'time_driving': 27, 'time_transit': 51}, (22, 27): {'time_driving': 14, 'time_transit': 36}, (18, 27): {'time_driving': 17, 'time_transit': 42}, (23, 2): {'time_driving': 7, 'time_transit': 24}, (8, 29): {'time_driving': 6, 'time_transit': 41}, (32, 10): {'time_driving': 22, 'time_transit': 41}, (9, 24): {'time_driving': 9, 'time_transit': 18}, (14, 23): {'time_driving': 7, 'time_transit': 14}, (12, 3): {'time_driving': 5, 'time_transit': 8}, (10, 31): {'time_driving': 18, 'time_transit': 21}, (25, 29): {'time_driving': 9, 'time_transit': 25}, (15, 22): {'time_driving': 12, 'time_transit': 18}, (13, 2): {'time_driving': 7, 'time_transit': 25}, (11, 30): {'time_driving': 19, 'time_transit': 29}, (24, 6): {'time_driving': 7, 'time_transit': 18}, (12, 25): {'time_driving': 7, 'time_transit': 14}, (27, 19): {'time_driving': 16, 'time_transit': 39}, (1, 4): {'time_driving': 16, 'time_transit': 25}, (25, 7): {'time_driving': 11, 'time_transit': 21}, (13, 28): {'time_driving': 5, 'time_transit': 17}, (28, 20): {'time_driving': 14, 'time_transit': 21}, (2, 3): {'time_driving': 2, 'time_transit': 2}, (26, 4): {'time_driving': 15, 'time_transit': 35}, (29, 25): {'time_driving': 12, 'time_transit': 29}, (3, 26): {'time_driving': 6, 'time_transit': 16}, (27, 9): {'time_driving': 16, 'time_transit': 27}, (6, 5): {'time_driving': 19, 'time_transit': 42}, (30, 6): {'time_driving': 18, 'time_transit': 41}, (4, 29): {'time_driving': 11, 'time_transit': 29}, (19, 31): {'time_driving': 14, 'time_transit': 34}, (31, 7): {'time_driving': 10, 'time_transit': 24}, (5, 16): {'time_driving': 5, 'time_transit': 16}, (20, 24): {'time_driving': 14, 'time_transit': 27}, (3, 32): {'time_driving': 21, 'time_transit': 48}, (16, 8): {'time_driving': 16, 'time_transit': 39}, (6, 31): {'time_driving': 18, 'time_transit': 25}, (21, 29): {'time_driving': 13, 'time_transit': 30}, (19, 5): {'time_driving': 4, 'time_transit': 9}, (17, 21): {'time_driving': 12, 'time_transit': 24}, (7, 30): {'time_driving': 15, 'time_transit': 37}, (22, 18): {'time_driving': 19, 'time_transit': 40}, (20, 6): {'time_driving': 14, 'time_transit': 22}, (23, 27): {'time_driving': 15, 'time_transit': 46}, (21, 7): {'time_driving': 10, 'time_transit': 20}, (8, 4): {'time_driving': 15, 'time_transit': 38}, (32, 1): {'time_driving': 18, 'time_transit': 34}, (9, 1): {'time_driving': 7, 'time_transit': 9}, (14, 30): {'time_driving': 19, 'time_transit': 37}, (10, 6): {'time_driving': 4, 'time_transit': 8}, (15, 31): {'time_driving': 16, 'time_transit': 15}, (11, 23): {'time_driving': 7, 'time_transit': 14}, (24, 13): {'time_driving': 6, 'time_transit': 27}, (12, 16): {'time_driving': 16, 'time_transit': 35}, (1, 29): {'time_driving': 7, 'time_transit': 32}, (25, 8): {'time_driving': 8, 'time_transit': 20}, (15, 5): {'time_driving': 17, 'time_transit': 24}, (13, 21): {'time_driving': 13, 'time_transit': 24}, (28, 19): {'time_driving': 17, 'time_transit': 48}, (2, 26): {'time_driving': 5, 'time_transit': 14}, (26, 15): {'time_driving': 8, 'time_transit': 16}, (29, 18): {'time_driving': 21, 'time_transit': 54}, (27, 14): {'time_driving': 12, 'time_transit': 28}, (30, 9): {'time_driving': 11, 'time_transit': 32}, (28, 9): {'time_driving': 11, 'time_transit': 22}, (31, 12): {'time_driving': 13, 'time_transit': 25}, (5, 25): {'time_driving': 19, 'time_transit': 32}, (29, 12): {'time_driving': 7, 'time_transit': 29}, (16, 15): {'time_driving': 22, 'time_transit': 40}, (6, 22): {'time_driving': 5, 'time_transit': 8}, (30, 19): {'time_driving': 19, 'time_transit': 55}, (19, 10): {'time_driving': 21, 'time_transit': 42}, (17, 14): {'time_driving': 9, 'time_transit': 19}, (7, 23): {'time_driving': 9, 'time_transit': 35}, (22, 21): {'time_driving': 12, 'time_transit': 21}, (20, 13): {'time_driving': 7, 'time_transit': 10}, (18, 13): {'time_driving': 16, 'time_transit': 45}, (23, 16): {'time_driving': 21, 'time_transit': 57}, (17, 32): {'time_driving': 17, 'time_transit': 47}, (32, 24): {'time_driving': 18, 'time_transit': 52}, (22, 15): {'time_driving': 9, 'time_transit': 15}, (9, 10): {'time_driving': 12, 'time_transit': 22}, (23, 14): {'time_driving': 6, 'time_transit': 18}, (10, 1): {'time_driving': 7, 'time_transit': 15}, (8, 17): {'time_driving': 10, 'time_transit': 14}, (11, 12): {'time_driving': 2, 'time_transit': 7}, (24, 20): {'time_driving': 13, 'time_transit': 27}, (14, 11): {'time_driving': 3, 'time_transit': 7}, (12, 15): {'time_driving': 5, 'time_transit': 9}, (1, 22): {'time_driving': 9, 'time_transit': 23}, (25, 17): {'time_driving': 14, 'time_transit': 20}, (15, 2): {'time_driving': 3, 'time_transit': 5}, (13, 14): {'time_driving': 7, 'time_transit': 26}, (2, 21): {'time_driving': 7, 'time_transit': 10}, (26, 22): {'time_driving': 7, 'time_transit': 29}, (3, 8): {'time_driving': 7, 'time_transit': 15}, (27, 7): {'time_driving': 4, 'time_transit': 5}, (1, 8): {'time_driving': 5, 'time_transit': 12}, (4, 3): {'time_driving': 17, 'time_transit': 27}, (2, 15): {'time_driving': 5, 'time_transit': 5}, (24, 32): {'time_driving': 18, 'time_transit': 53}, (5, 2): {'time_driving': 14, 'time_transit': 29}, (29, 5): {'time_driving': 18, 'time_transit': 59}, (16, 6): {'time_driving': 24, 'time_transit': 50}, (6, 9): {'time_driving': 15, 'time_transit': 25}, (17, 11): {'time_driving': 9, 'time_transit': 16}, (17, 7): {'time_driving': 1, 'time_transit': 2}, (7, 12): {'time_driving': 7, 'time_transit': 21}, (31, 19): {'time_driving': 14, 'time_transit': 30}, (18, 4): {'time_driving': 24, 'time_transit': 48}, (16, 28): {'time_driving': 22, 'time_transit': 51}, (21, 9): {'time_driving': 4, 'time_transit': 4}, (17, 25): {'time_driving': 12, 'time_transit': 24}, (32, 31): {'time_driving': 14, 'time_transit': 33}, (22, 6): {'time_driving': 5, 'time_transit': 9}, (18, 30): {'time_driving': 10, 'time_transit': 18}, (23, 7): {'time_driving': 12, 'time_transit': 45}, (10, 8): {'time_driving': 10, 'time_transit': 26}, (8, 24): {'time_driving': 3, 'time_transit': 16}, (11, 5): {'time_driving': 15, 'time_transit': 20}, (9, 21): {'time_driving': 2, 'time_transit': 4}, (24, 27): {'time_driving': 11, 'time_transit': 29}, (14, 18): {'time_driving': 14, 'time_transit': 33}, (12, 6): {'time_driving': 7, 'time_transit': 18}, (10, 18): {'time_driving': 15, 'time_transit': 36}, (25, 26): {'time_driving': 8, 'time_transit': 14}, (15, 11): {'time_driving': 3, 'time_transit': 2}, (13, 7): {'time_driving': 12, 'time_transit': 41}, (11, 27): {'time_driving': 11, 'time_transit': 23}, (26, 17): {'time_driving': 14, 'time_transit': 44}, (24, 1): {'time_driving': 3, 'time_transit': 8}, (12, 28): {'time_driving': 5, 'time_transit': 17}, (27, 28): {'time_driving': 13, 'time_transit': 36}, (4, 10): {'time_driving': 16, 'time_transit': 21}, (28, 31): {'time_driving': 15, 'time_transit': 25}, (2, 6): {'time_driving': 7, 'time_transit': 13}, (5, 11): {'time_driving': 15, 'time_transit': 25}, (29, 30): {'time_driving': 21, 'time_transit': 58}, (3, 23): {'time_driving': 7, 'time_transit': 18}, (30, 29): {'time_driving': 21, 'time_transit': 50}, (4, 16): {'time_driving': 29, 'time_transit': 62}, (19, 24): {'time_driving': 17, 'time_transit': 46}, (2, 32): {'time_driving': 18, 'time_transit': 46}, (7, 5): {'time_driving': 11, 'time_transit': 20}, (31, 24): {'time_driving': 13, 'time_transit': 25}, (5, 21): {'time_driving': 18, 'time_transit': 31}, (20, 19): {'time_driving': 26, 'time_transit': 51}, (16, 19): {'time_driving': 3, 'time_transit': 4}, (6, 26): {'time_driving': 9, 'time_transit': 16}, (21, 18): {'time_driving': 9, 'time_transit': 22}, (17, 18): {'time_driving': 17, 'time_transit': 44}, (32, 22): {'time_driving': 22, 'time_transit': 53}, (22, 25): {'time_driving': 11, 'time_transit': 18}, (30, 21): {'time_driving': 12, 'time_transit': 32}, (18, 25): {'time_driving': 13, 'time_transit': 20}, (23, 28): {'time_driving': 7, 'time_transit': 15}, (8, 31): {'time_driving': 10, 'time_transit': 28}, (32, 12): {'time_driving': 18, 'time_transit': 52}, (9, 30): {'time_driving': 13, 'time_transit': 23}, (14, 21): {'time_driving': 9, 'time_transit': 12}, (10, 29): {'time_driving': 7, 'time_transit': 17}, (15, 16): {'time_driving': 21, 'time_transit': 33}, (11, 16): {'time_driving': 18, 'time_transit': 28}, (26, 24): {'time_driving': 5, 'time_transit': 20}, (24, 8): {'time_driving': 4, 'time_transit': 17}, (12, 27): {'time_driving': 11, 'time_transit': 29}, (27, 21): {'time_driving': 15, 'time_transit': 23}, (1, 26): {'time_driving': 5, 'time_transit': 21}, (25, 5): {'time_driving': 17, 'time_transit': 27}, (13, 26): {'time_driving': 7, 'time_transit': 32}, (28, 22): {'time_driving': 7, 'time_transit': 11}, (2, 1): {'time_driving': 1, 'time_transit': 2}, (26, 2): {'time_driving': 6, 'time_transit': 22}, (29, 23): {'time_driving': 9, 'time_transit': 33}, (3, 28): {'time_driving': 8, 'time_transit': 12}, (27, 11): {'time_driving': 12, 'time_transit': 24}, (30, 4): {'time_driving': 28, 'time_transit': 46}, (4, 31): {'time_driving': 24, 'time_transit': 33}, (28, 12): {'time_driving': 5, 'time_transit': 17}, (7, 2): {'time_driving': 6, 'time_transit': 13}, (31, 1): {'time_driving': 14, 'time_transit': 17}, (5, 30): {'time_driving': 18, 'time_transit': 60}, (20, 26): {'time_driving': 15, 'time_transit': 33}, (16, 10): {'time_driving': 23, 'time_transit': 46}, (6, 29): {'time_driving': 3, 'time_transit': 11}, (21, 27): {'time_driving': 12, 'time_transit': 21}, (19, 7): {'time_driving': 14, 'time_transit': 37}, (8, 32): {'time_driving': 16, 'time_transit': 52}, (7, 24): {'time_driving': 7, 'time_transit': 21}, (22, 16): {'time_driving': 20, 'time_transit': 57}, (18, 16): {'time_driving': 22, 'time_transit': 72}, (16, 32): {'time_driving': 5, 'time_transit': 12}, (21, 5): {'time_driving': 16, 'time_transit': 34}, (8, 6): {'time_driving': 7, 'time_transit': 26}, (32, 3): {'time_driving': 19, 'time_transit': 48}, (22, 10): {'time_driving': 8, 'time_transit': 14}, (9, 7): {'time_driving': 11, 'time_transit': 25}, (14, 28): {'time_driving': 6, 'time_transit': 10}, (10, 4): {'time_driving': 16, 'time_transit': 20}, (15, 25): {'time_driving': 3, 'time_transit': 5}, (11, 9): {'time_driving': 8, 'time_transit': 10}, (24, 15): {'time_driving': 5, 'time_transit': 9}, (14, 6): {'time_driving': 6, 'time_transit': 14}, (12, 18): {'time_driving': 12, 'time_transit': 34}, (1, 19): {'time_driving': 14, 'time_transit': 34}, (25, 14): {'time_driving': 6, 'time_transit': 10}, (15, 7): {'time_driving': 11, 'time_transit': 22}, (13, 19): {'time_driving': 18, 'time_transit': 52}, (2, 24): {'time_driving': 1, 'time_transit': 7}, (26, 13): {'time_driving': 7, 'time_transit': 31}, (29, 16): {'time_driving': 21, 'time_transit': 71}, (3, 5): {'time_driving': 15, 'time_transit': 24}, (30, 15): {'time_driving': 15, 'time_transit': 22}, (4, 6): {'time_driving': 14, 'time_transit': 24}, (28, 11): {'time_driving': 6, 'time_transit': 11}, (31, 14): {'time_driving': 14, 'time_transit': 24}, (5, 7): {'time_driving': 11, 'time_transit': 22}, (29, 10): {'time_driving': 9, 'time_transit': 17}, (16, 1): {'time_driving': 19, 'time_transit': 35}, (6, 20): {'time_driving': 11, 'time_transit': 21}, (29, 11): {'time_driving': 8, 'time_transit': 23}, (19, 12): {'time_driving': 17, 'time_transit': 46}, (17, 12): {'time_driving': 8, 'time_transit': 22}, (7, 17): {'time_driving': 4, 'time_transit': 2}, (31, 20): {'time_driving': 21, 'time_transit': 31}, (20, 15): {'time_driving': 17, 'time_transit': 17}, (18, 11): {'time_driving': 15, 'time_transit': 25}, (23, 18): {'time_driving': 14, 'time_transit': 41}, (21, 14): {'time_driving': 10, 'time_transit': 15}, (8, 13): {'time_driving': 7, 'time_transit': 41}, (32, 26): {'time_driving': 19, 'time_transit': 54}, (22, 13): {'time_driving': 1, 'time_transit': 3}, (9, 8): {'time_driving': 8, 'time_transit': 20}, (23, 8): {'time_driving': 8, 'time_transit': 31}, (10, 15): {'time_driving': 6, 'time_transit': 7}, (8, 19): {'time_driving': 12, 'time_transit': 37}, (11, 14): {'time_driving': 4, 'time_transit': 5}, (9, 18): {'time_driving': 9, 'time_transit': 24}, (24, 22): {'time_driving': 7, 'time_transit': 24}, (14, 9): {'time_driving': 10, 'time_transit': 19}, (12, 9): {'time_driving': 9, 'time_transit': 20}, (1, 20): {'time_driving': 15, 'time_transit': 24}, (25, 23): {'time_driving': 9, 'time_transit': 16}, (15, 12): {'time_driving': 4, 'time_transit': 9}, (13, 12): {'time_driving': 6, 'time_transit': 30}, (2, 19): {'time_driving': 14, 'time_transit': 31}, (26, 20): {'time_driving': 14, 'time_transit': 35}, (3, 10): {'time_driving': 7, 'time_transit': 13}, (27, 25): {'time_driving': 16, 'time_transit': 23}, (1, 14): {'time_driving': 5, 'time_transit': 8}, (4, 13): {'time_driving': 10, 'time_transit': 17}, (28, 2): {'time_driving': 6, 'time_transit': 12}, (2, 13): {'time_driving': 7, 'time_transit': 23}, (29, 3): {'time_driving': 10, 'time_transit': 26}, (3, 16): {'time_driving': 19, 'time_transit': 33}, (1, 32): {'time_driving': 18, 'time_transit': 34}, (6, 15): {'time_driving': 8, 'time_transit': 14}, (30, 24): {'time_driving': 13, 'time_transit': 31}, (19, 21): {'time_driving': 21, 'time_transit': 38}, (17, 5): {'time_driving': 12, 'time_transit': 20}, (7, 14): {'time_driving': 8, 'time_transit': 18}, (31, 29): {'time_driving': 16, 'time_transit': 40}, (20, 22): {'time_driving': 8, 'time_transit': 14}, (18, 2): {'time_driving': 11, 'time_transit': 26}, (16, 30): {'time_driving': 23, 'time_transit': 64}, (21, 23): {'time_driving': 13, 'time_transit': 25}, (17, 31): {'time_driving': 11, 'time_transit': 23}, (32, 17): {'time_driving': 18, 'time_transit': 42}, (22, 4): {'time_driving': 11, 'time_transit': 17}, (18, 28): {'time_driving': 20, 'time_transit': 40}, (23, 1): {'time_driving': 7, 'time_transit': 27}, (8, 26): {'time_driving': 4, 'time_transit': 27}, (11, 7): {'time_driving': 9, 'time_transit': 12}, (9, 27): {'time_driving': 13, 'time_transit': 26}, (24, 29): {'time_driving': 6, 'time_transit': 27}, (14, 16): {'time_driving': 18, 'time_transit': 36}, (10, 16): {'time_driving': 22, 'time_transit': 47}, (25, 24): {'time_driving': 4, 'time_transit': 10}, (15, 21): {'time_driving': 6, 'time_transit': 10}, (13, 5): {'time_driving': 17, 'time_transit': 51}, (11, 29): {'time_driving': 7, 'time_transit': 21}, (26, 31): {'time_driving': 15, 'time_transit': 37}, (28, 30): {'time_driving': 20, 'time_transit': 41}, (24, 3): {'time_driving': 5, 'time_transit': 8}, (12, 30): {'time_driving': 17, 'time_transit': 36}, (27, 30): {'time_driving': 19, 'time_transit': 43}, (1, 7): {'time_driving': 7, 'time_transit': 18}, (25, 2): {'time_driving': 3, 'time_transit': 6}, (13, 31): {'time_driving': 16, 'time_transit': 36}, (28, 25): {'time_driving': 10, 'time_transit': 17}, (2, 4): {'time_driving': 15, 'time_transit': 25}, (5, 9): {'time_driving': 20, 'time_transit': 34}, (29, 28): {'time_driving': 6, 'time_transit': 15}, (3, 25): {'time_driving': 5, 'time_transit': 8}, (30, 3): {'time_driving': 15, 'time_transit': 28}, (4, 18): {'time_driving': 24, 'time_transit': 42}, (19, 26): {'time_driving': 18, 'time_transit': 50}, (31, 26): {'time_driving': 14, 'time_transit': 37}, (5, 19): {'time_driving': 2, 'time_transit': 8}, (20, 29): {'time_driving': 10, 'time_transit': 23}, (16, 21): {'time_driving': 23, 'time_transit': 42}, (6, 24): {'time_driving': 8, 'time_transit': 19}, (21, 16): {'time_driving': 20, 'time_transit': 44}, (17, 16): {'time_driving': 16, 'time_transit': 29}, (7, 29): {'time_driving': 10, 'time_transit': 39}, (22, 31): {'time_driving': 16, 'time_transit': 29}, (18, 23): {'time_driving': 15, 'time_transit': 45}, (23, 30): {'time_driving': 19, 'time_transit': 59}, (8, 1): {'time_driving': 3, 'time_transit': 12}, (32, 14): {'time_driving': 19, 'time_transit': 44}, (30, 17): {'time_driving': 18, 'time_transit': 36}, (9, 28): {'time_driving': 12, 'time_transit': 24}, (14, 27): {'time_driving': 13, 'time_transit': 29}, (10, 27): {'time_driving': 15, 'time_transit': 33}, (15, 18): {'time_driving': 12, 'time_transit': 22}, (11, 18): {'time_driving': 13, 'time_transit': 25}, (24, 10): {'time_driving': 6, 'time_transit': 17}, (12, 21): {'time_driving': 9, 'time_transit': 17}, (27, 23): {'time_driving': 13, 'time_transit': 47}, (1, 24): {'time_driving': 2, 'time_transit': 8}, (25, 11): {'time_driving': 2, 'time_transit': 5}, (13, 24): {'time_driving': 6, 'time_transit': 30}, (28, 16): {'time_driving': 20, 'time_transit': 49}, (2, 31): {'time_driving': 12, 'time_transit': 19}, (29, 21): {'time_driving': 13, 'time_transit': 32}, (3, 30): {'time_driving': 19, 'time_transit': 33}, (27, 13): {'time_driving': 14, 'time_transit': 45}, (8, 11): {'time_driving': 4, 'time_transit': 16}, (30, 10): {'time_driving': 15, 'time_transit': 34}, (4, 25): {'time_driving': 19, 'time_transit': 23}, (28, 14): {'time_driving': 6, 'time_transit': 13}, (31, 3): {'time_driving': 15, 'time_transit': 21}, (5, 28): {'time_driving': 17, 'time_transit': 41}, (29, 15): {'time_driving': 10, 'time_transit': 29}, (16, 12): {'time_driving': 19, 'time_transit': 44}, (6, 19): {'time_driving': 20, 'time_transit': 48}, (21, 25): {'time_driving': 4, 'time_transit': 6}, (19, 9): {'time_driving': 23, 'time_transit': 43}, (17, 9): {'time_driving': 13, 'time_transit': 27}, (7, 26): {'time_driving': 8, 'time_transit': 33}, (20, 2): {'time_driving': 15, 'time_transit': 30}, (18, 14): {'time_driving': 11, 'time_transit': 31}, (21, 3): {'time_driving': 7, 'time_transit': 10}, (32, 5): {'time_driving': 8, 'time_transit': 16}, (22, 8): {'time_driving': 8, 'time_transit': 36}, (9, 5): {'time_driving': 17, 'time_transit': 39}, (23, 13): {'time_driving': 8, 'time_transit': 32}, (10, 2): {'time_driving': 6, 'time_transit': 12}, (15, 27): {'time_driving': 14, 'time_transit': 23}, (24, 17): {'time_driving': 11, 'time_transit': 19}, (14, 4): {'time_driving': 16, 'time_transit': 28}, (1, 17): {'time_driving': 10, 'time_transit': 18}, (25, 12): {'time_driving': 4, 'time_transit': 10}, (15, 1): {'time_driving': 5, 'time_transit': 5}, (13, 17): {'time_driving': 15, 'time_transit': 41}, (2, 22): {'time_driving': 8, 'time_transit': 20}, (26, 11): {'time_driving': 6, 'time_transit': 20}, (3, 7): {'time_driving': 9, 'time_transit': 16}, (27, 2): {'time_driving': 10, 'time_transit': 22}, (1, 11): {'time_driving': 3, 'time_transit': 5}, (30, 13): {'time_driving': 22, 'time_transit': 45}, (28, 5): {'time_driving': 16, 'time_transit': 43}, (31, 8): {'time_driving': 10, 'time_transit': 27}, (29, 8): {'time_driving': 9, 'time_transit': 39}, (16, 3): {'time_driving': 20, 'time_transit': 37}, (6, 10): {'time_driving': 5, 'time_transit': 7}, (30, 23): {'time_driving': 21, 'time_transit': 46}, (19, 14): {'time_driving': 18, 'time_transit': 45}, (17, 2): {'time_driving': 7, 'time_transit': 14}, (7, 19): {'time_driving': 12, 'time_transit': 29}, (31, 22): {'time_driving': 17, 'time_transit': 31}, (20, 9): {'time_driving': 16, 'time_transit': 23}, (18, 9): {'time_driving': 8, 'time_transit': 20}, (16, 25): {'time_driving': 24, 'time_transit': 42}, (21, 12): {'time_driving': 8, 'time_transit': 14}, (8, 15): {'time_driving': 6, 'time_transit': 18}, (32, 28): {'time_driving': 21, 'time_transit': 45}, (22, 3): {'time_driving': 8, 'time_transit': 23}, (9, 14): {'time_driving': 11, 'time_transit': 16}, (23, 10): {'time_driving': 9, 'time_transit': 17}, (10, 13): {'time_driving': 8, 'time_transit': 17}, (8, 21): {'time_driving': 7, 'time_transit': 20}, (9, 16): {'time_driving': 21, 'time_transit': 46}, (14, 15): {'time_driving': 3, 'time_transit': 3}, (12, 11): {'time_driving': 3, 'time_transit': 7}, (10, 23): {'time_driving': 11, 'time_transit': 20}, (25, 21): {'time_driving': 5, 'time_transit': 6}, (15, 14): {'time_driving': 4, 'time_transit': 7}, (13, 10): {'time_driving': 8, 'time_transit': 18}, (2, 17): {'time_driving': 10, 'time_transit': 15}, (26, 18): {'time_driving': 13, 'time_transit': 41}, (3, 12): {'time_driving': 2, 'time_transit': 8}, (1, 12): {'time_driving': 2, 'time_transit': 8}, (4, 15): {'time_driving': 17, 'time_transit': 19}, (2, 11): {'time_driving': 3, 'time_transit': 1}, (5, 14): {'time_driving': 15, 'time_transit': 36}, (29, 1): {'time_driving': 8, 'time_transit': 27}, (3, 18): {'time_driving': 12, 'time_transit': 28}, (6, 13): {'time_driving': 4, 'time_transit': 11}, (4, 21): {'time_driving': 21, 'time_transit': 27}, (19, 23): {'time_driving': 19, 'time_transit': 52}, (7, 8): {'time_driving': 4, 'time_transit': 14}, (22, 32): {'time_driving': 21, 'time_transit': 56}, (20, 16): {'time_driving': 29, 'time_transit': 60}, (30, 32): {'time_driving': 20, 'time_transit': 54}, (17, 29): {'time_driving': 10, 'time_transit': 40}, (32, 19): {'time_driving': 2, 'time_transit': 8}, (22, 26): {'time_driving': 7, 'time_transit': 27}, (9, 32): {'time_driving': 17, 'time_transit': 44}, (18, 26): {'time_driving': 14, 'time_transit': 43}, (23, 3): {'time_driving': 8, 'time_transit': 26}, (8, 28): {'time_driving': 5, 'time_transit': 24}, (32, 9): {'time_driving': 21, 'time_transit': 44}, (32, 21): {'time_driving': 22, 'time_transit': 40}, (9, 25): {'time_driving': 6, 'time_transit': 10}, (24, 31): {'time_driving': 12, 'time_transit': 25}, (14, 22): {'time_driving': 8, 'time_transit': 17}, (12, 2): {'time_driving': 3, 'time_transit': 6}, (10, 30): {'time_driving': 20, 'time_transit': 42}, (25, 30): {'time_driving': 16, 'time_transit': 24}, (15, 23): {'time_driving': 9, 'time_transit': 14}, (13, 3): {'time_driving': 9, 'time_transit': 27}, (11, 31): {'time_driving': 16, 'time_transit': 18}, (26, 29): {'time_driving': 6, 'time_transit': 30}, (24, 5): {'time_driving': 13, 'time_transit': 26}, (12, 24): {'time_driving': 1, 'time_transit': 1}, (27, 16): {'time_driving': 19, 'time_transit': 38}, (1, 5): {'time_driving': 13, 'time_transit': 22}, (13, 29): {'time_driving': 2, 'time_transit': 5}, (28, 27): {'time_driving': 14, 'time_transit': 37}, (26, 7): {'time_driving': 11, 'time_transit': 42}, (29, 26): {'time_driving': 8, 'time_transit': 31}, (3, 27): {'time_driving': 12, 'time_transit': 27}, (6, 4): {'time_driving': 12, 'time_transit': 19}, (30, 1): {'time_driving': 14, 'time_transit': 27}, (4, 28): {'time_driving': 13, 'time_transit': 24}, (19, 28): {'time_driving': 19, 'time_transit': 46}, (7, 1): {'time_driving': 6, 'time_transit': 13}, (31, 4): {'time_driving': 25, 'time_transit': 33}, (5, 17): {'time_driving': 14, 'time_transit': 23}, (20, 31): {'time_driving': 20, 'time_transit': 31}, (16, 23): {'time_driving': 22, 'time_transit': 61}, (6, 30): {'time_driving': 22, 'time_transit': 42}, (21, 30): {'time_driving': 14, 'time_transit': 23}, (19, 2): {'time_driving': 17, 'time_transit': 38}, (17, 22): {'time_driving': 12, 'time_transit': 37}, (7, 31): {'time_driving': 10, 'time_transit': 22}, (22, 29): {'time_driving': 2, 'time_transit': 9}, (20, 5): {'time_driving': 25, 'time_transit': 51}, (18, 21): {'time_driving': 9, 'time_transit': 23}, (23, 24): {'time_driving': 6, 'time_transit': 23}, (8, 3): {'time_driving': 4, 'time_transit': 15}, (9, 2): {'time_driving': 7, 'time_transit': 13}, (14, 25): {'time_driving': 6, 'time_transit': 6}, (10, 25): {'time_driving': 9, 'time_transit': 11}, (15, 28): {'time_driving': 8, 'time_transit': 13}, (11, 20): {'time_driving': 15, 'time_transit': 20}, (24, 12): {'time_driving': 2, 'time_transit': 1}, (14, 3): {'time_driving': 6, 'time_transit': 10}, (12, 23): {'time_driving': 5, 'time_transit': 16}, (1, 30): {'time_driving': 17, 'time_transit': 27}, (25, 9): {'time_driving': 7, 'time_transit': 9}, (13, 22): {'time_driving': 1, 'time_transit': 3}, (28, 18): {'time_driving': 14, 'time_transit': 40}, (2, 29): {'time_driving': 6, 'time_transit': 23}, (26, 14): {'time_driving': 5, 'time_transit': 16}, (29, 19): {'time_driving': 19, 'time_transit': 60}, (27, 15): {'time_driving': 14, 'time_transit': 22}, (15, 32): {'time_driving': 20, 'time_transit': 35}, (30, 8): {'time_driving': 15, 'time_transit': 40}, (4, 27): {'time_driving': 23, 'time_transit': 40}, (28, 8): {'time_driving': 7, 'time_transit': 26}, (31, 13): {'time_driving': 17, 'time_transit': 32}, (5, 26): {'time_driving': 15, 'time_transit': 44}, (29, 13): {'time_driving': 3, 'time_transit': 5}, (16, 14): {'time_driving': 20, 'time_transit': 42}, (6, 17): {'time_driving': 17, 'time_transit': 36}, (30, 18): {'time_driving': 9, 'time_transit': 18}, (19, 11): {'time_driving': 18, 'time_transit': 40}, (17, 15): {'time_driving': 11, 'time_transit': 23}, (7, 20): {'time_driving': 18, 'time_transit': 35}, (22, 20): {'time_driving': 7, 'time_transit': 13}, (20, 12): {'time_driving': 14, 'time_transit': 27}, (18, 12): {'time_driving': 10, 'time_transit': 33}, (23, 17): {'time_driving': 15, 'time_transit': 47}, (21, 1): {'time_driving': 6, 'time_transit': 9}, (8, 10): {'time_driving': 7, 'time_transit': 25}, (32, 7): {'time_driving': 15, 'time_transit': 42}, (22, 14): {'time_driving': 7, 'time_transit': 22}, (9, 11): {'time_driving': 7, 'time_transit': 10}, (23, 15): {'time_driving': 9, 'time_transit': 18}, (8, 16): {'time_driving': 15, 'time_transit': 36}, (11, 13): {'time_driving': 8, 'time_transit': 22}, (24, 19): {'time_driving': 14, 'time_transit': 35}, (14, 10): {'time_driving': 5, 'time_transit': 11}, (12, 14): {'time_driving': 3, 'time_transit': 10}, (1, 23): {'time_driving': 7, 'time_transit': 23}, (25, 18): {'time_driving': 12, 'time_transit': 20}, (15, 3): {'time_driving': 6, 'time_transit': 7}, (13, 15): {'time_driving': 9, 'time_transit': 21}, (2, 20): {'time_driving': 14, 'time_transit': 24}, (26, 9): {'time_driving': 10, 'time_transit': 31}, (28, 13): {'time_driving': 7, 'time_transit': 15}, (3, 9): {'time_driving': 9, 'time_transit': 15}, (27, 4): {'time_driving': 22, 'time_transit': 40}, (1, 9): {'time_driving': 8, 'time_transit': 9}, (4, 2): {'time_driving': 15, 'time_transit': 25}, (28, 7): {'time_driving': 11, 'time_transit': 36}, (2, 14): {'time_driving': 3, 'time_transit': 6}, (31, 10): {'time_driving': 16, 'time_transit': 21}, (5, 3): {'time_driving': 15, 'time_transit': 31}, (29, 6): {'time_driving': 7, 'time_transit': 12}, (16, 5): {'time_driving': 6, 'time_transit': 14}, (6, 8): {'time_driving': 10, 'time_transit': 28}, (21, 32): {'time_driving': 17, 'time_transit': 38}, (19, 16): {'time_driving': 1, 'time_transit': 4}, (7, 13): {'time_driving': 10, 'time_transit': 44}, (31, 16): {'time_driving': 17, 'time_transit': 39}, (20, 11): {'time_driving': 15, 'time_transit': 20}, (18, 7): {'time_driving': 14, 'time_transit': 41}, (16, 27): {'time_driving': 19, 'time_transit': 44}, (21, 10): {'time_driving': 11, 'time_transit': 15}, (17, 26): {'time_driving': 9, 'time_transit': 33}, (32, 30): {'time_driving': 19, 'time_transit': 59}, (22, 1): {'time_driving': 7, 'time_transit': 24}, (9, 12): {'time_driving': 9, 'time_transit': 18}, (23, 4): {'time_driving': 16, 'time_transit': 38}, (10, 11): {'time_driving': 6, 'time_transit': 11}, (8, 23): {'time_driving': 5, 'time_transit': 31}, (11, 2): {'time_driving': 1, 'time_transit': 1}, (9, 22): {'time_driving': 16, 'time_transit': 20}, (24, 26): {'time_driving': 4, 'time_transit': 14}, (14, 13): {'time_driving': 8, 'time_transit': 21}, (12, 5): {'time_driving': 13, 'time_transit': 26}, (10, 21): {'time_driving': 11, 'time_transit': 20}, (25, 27): {'time_driving': 13, 'time_transit': 23}, (15, 8): {'time_driving': 9, 'time_transit': 18}, (13, 8): {'time_driving': 8, 'time_transit': 40}, (11, 24): {'time_driving': 2, 'time_transit': 7}, (26, 16): {'time_driving': 20, 'time_transit': 54}, (3, 14): {'time_driving': 4, 'time_transit': 7}, (27, 29): {'time_driving': 14, 'time_transit': 50}, (1, 2): {'time_driving': 1, 'time_transit': 2}, (4, 9): {'time_driving': 20, 'time_transit': 35}, (23, 21): {'time_driving': 13, 'time_transit': 28}, (2, 9): {'time_driving': 9, 'time_transit': 13}, (5, 12): {'time_driving': 14, 'time_transit': 31}, (29, 31): {'time_driving': 17, 'time_transit': 40}, (3, 20): {'time_driving': 15, 'time_transit': 24}, (6, 3): {'time_driving': 11, 'time_transit': 16}, (30, 28): {'time_driving': 21, 'time_transit': 38}, (4, 23): {'time_driving': 17, 'time_transit': 37}, (19, 25): {'time_driving': 22, 'time_transit': 40}, (7, 10): {'time_driving': 11, 'time_transit': 24}, (31, 25): {'time_driving': 15, 'time_transit': 20}, (5, 22): {'time_driving': 18, 'time_transit': 53}, (20, 18): {'time_driving': 18, 'time_transit': 39}, (16, 18): {'time_driving': 28, 'time_transit': 68}, (21, 19): {'time_driving': 17, 'time_transit': 35}, (17, 19): {'time_driving': 13, 'time_transit': 29}, (7, 32): {'time_driving': 16, 'time_transit': 46}, (22, 24): {'time_driving': 6, 'time_transit': 26}, (31, 32): {'time_driving': 14, 'time_transit': 44}, (18, 24): {'time_driving': 10, 'time_transit': 33}, (23, 29): {'time_driving': 7, 'time_transit': 32}, (8, 30): {'time_driving': 15, 'time_transit': 40}, (32, 11): {'time_driving': 19, 'time_transit': 36}, (9, 31): {'time_driving': 13, 'time_transit': 26}, (14, 20): {'time_driving': 15, 'time_transit': 26}, (10, 28): {'time_driving': 4, 'time_transit': 8}, (25, 28): {'time_driving': 9, 'time_transit': 16}, (15, 17): {'time_driving': 14, 'time_transit': 17}, (13, 1): {'time_driving': 7, 'time_transit': 28}, (11, 17): {'time_driving': 12, 'time_transit': 13}, (26, 27): {'time_driving': 14, 'time_transit': 43}, (24, 7): {'time_driving': 8, 'time_transit': 18}, (12, 26): {'time_driving': 4, 'time_transit': 14}, (27, 18): {'time_driving': 20, 'time_transit': 46}, (1, 27): {'time_driving': 10, 'time_transit': 22}, (25, 6): {'time_driving': 9, 'time_transit': 16}, (13, 27): {'time_driving': 14, 'time_transit': 42}, (28, 21): {'time_driving': 12, 'time_transit': 23}, (26, 5): {'time_driving': 16, 'time_transit': 58}, (14, 32): {'time_driving': 20, 'time_transit': 49}, (29, 24): {'time_driving': 7, 'time_transit': 29}, (3, 29): {'time_driving': 8, 'time_transit': 25}, (27, 8): {'time_driving': 8, 'time_transit': 22}, (30, 7): {'time_driving': 15, 'time_transit': 36}, (4, 30): {'time_driving': 29, 'time_transit': 51}, (19, 30): {'time_driving': 20, 'time_transit': 58}}

def transit_time(from_index, to_index, from_df, to_df, transit_mode):
    '''
    Get the transit time between two spots, transit_mode includs 'transit', 'driving'

    Inputs:
        from_index, to_index: integer
        from_df, to_df: dataframes
        transit_mode: string, "driving" or "transit"

    Outputs:
        transit_time: int (minutes)
    '''
    gmaps = googlemaps.Client(key='AIzaSyCaHWPcxxYS4MCt9eLILdU7E0rdsmiBVSc')
    start = from_df.loc[from_index][0]
    end = to_df.loc[to_index][0]

    print(start, end)
    distance_result = gmaps.distance_matrix(start, end, mode=transit_mode, departure_time=T)
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
    print(transit_time)
    return transit_time


def select_attraction(df, pref_input, day=1):
    '''
    Selection a list of recommended attractions based on user
    preferences.

    Inputs:
        df: ATTRACTIONS dataframe
        pref_input: list of strings (0/1/2/3 ordered preferences)
        day: int (1 or 2)

    Output:
        list of tuple (attraction index, time needed)
    '''
    if day == 1:
        threshold = (6, 8)  #[6,8]
    else:
        threshold = (12, 15)  #[12,15]
    
    pref_n = len(pref_input)
    
    prefs = []
    sum_hours = 0
    selected = []
  
    if pref_n >= 1:
        prefs.append([df[pref_input[0]] == 1, 
            df[pref_input[0]] == 0])
        
        if pref_n >= 2:
            prefs.append([df[pref_input[1]] == 1, 
                df[pref_input[1]] == 0])
        
            if pref_n >= 3:
                prefs.append([df[pref_input[2]] == 1, 
                    df[pref_input[2]] == 0])
    
    criteria = [[[0],[1]],[(0,0),(0,1),(1,0),(1,1)],
                [(0,0,0),(0,0,1),(0,1,0),(1,0,0),
                (0,1,1),(1,0,1),(1,1,0),(1,1,1)]]
    
    for i in range(2**pref_n):
        if pref_n == 0:
            df_select = df
        else:
            c = criteria[pref_n-1][i]
            select = prefs[0][c[0]]
            for j in range(1, pref_n):
                select = select & prefs[j][c[j]]
            df_select = df[select]
        
        similar = 0               
        for row in df_select.itertuples():
            sum_hours += row[2]
            if sum_hours > threshold[1]:
                sum_hours -= row[2]
                if sum_hours < threshold[0]:
                    continue
                return selected
            selected.append((row[0], row[2]))
            similar += 1
            if pref_n > 0 and i == 0 and similar > 3:
                break
            if 0 < i < 2**pref_n-1 and similar > 1:
                break


def decide_next_spot(start, to_visit, from_df, to_df, transit_mode, stored = False):
    '''
    Given a start point, find the next spot to visit -
    based on the fact that it takes the least time to get there.

    Inputs:
        start: int, index of ATTRACTIONS/LOCATIONS
        to_visit: list of tuples representing attractions to visit
        from_df, to_df: ATTRACTIONS or LOCATIONS dataframe
        transit_mode: string, "driving" or "transit"
        stored: Boolean, True if it from_df and to_df are both ATTRACTIONS

    Output:
        (tuple representing next spot, list of remaining spots),
        int-time to travel to next spot

    '''
    next_ = 0
    min_ = 1000
    for i in range(len(to_visit)):
        if not stored:
            time = transit_time(start, to_visit[i][0], from_df, to_df, transit_mode)
        else:
            time = STORED[(start, to_visit[i][0])]["time_"+transit_mode]
        if time < min_:
            min_ = time
            next_ = i
    next_spot = to_visit[next_]
    new_to_visit = to_visit[:next_] + to_visit[next_+1:]
    
    return (next_spot, new_to_visit), min_


def single_day_route(visited, to_visit, transit_mode, total_t = 0):
    '''
    Decide the itinerary for a 1-day route.

    Inputs:
        visited: list of tuples,visited attractions
        to_visit: list of tuples,attractions to visit
        transit_mode: string, "driving" or "transit"
        total_t: time spent on travel from first to final attraction

    Output:
        list of attractions in order of travel,
        int (total travel time from first to final attraction)
    '''
    if len(to_visit) == 0:
        return visited, total_t
    
    (next_spot, to_visit), t = decide_next_spot(visited[-1][0], 
        to_visit, ATTRACTIONS, ATTRACTIONS, transit_mode, stored = True)
    visited.append(next_spot)
    total_t += t
    
    return single_day_route(visited, to_visit, transit_mode, total_t)


def first_day_route(visited, to_visit, transit_mode, sum_hours = 0, total_t = 0, t = 0, popped = None):
    '''
    For a 2-day itinerary, decide the 1st-day route.

    Inputs:
        visited: list of tuples,visited attractions
        to_visit: list of tuples,attractions to visit
        transit_mode: string, "driving" or "transit"
        sum_hours: float, total time spent on 1st-day attractions
        total_t: time spent on travel from first to final attraction
        t: travel time between the last 2 attractions in visited
        popped: None or list containing discarded attraction for day 1

    Output:
        ([list representing day-1 itinerary, time spent on travel from first to last
            attraction during day-1]), list of attractions to visit on day-2
    '''
    if popped is None:
        popped = []
    
    if len(visited) == 1:
        sum_hours = visited[0][1]

    if sum_hours > 8:
        place = visited.pop()
        popped.append(place)
        sum_hours -= place[1]
        total_t -= t     
        if sum_hours >= 6:
            return (visited, total_t), to_visit+popped
        if len(to_visit) == 0:
            total_t += STORED[(visited[-1][0],popped[0][0])]["time_"+transit_mode]
            return (visited+popped[0], total_t), popped[1:]
   
    (next_spot, to_visit), t = decide_next_spot(visited[-1][0],
        to_visit, ATTRACTIONS, ATTRACTIONS, transit_mode, stored=True)
    sum_hours += next_spot[1]
    visited.append(next_spot)
    total_t += t

    return first_day_route(visited, to_visit, transit_mode, sum_hours, total_t, t, popped)


def possible_routes(all_to_visit, transit_mode, day=1):
    '''
    Given a full list of attractions to visit, take any one of them as
    the first place to visit, calculate the corresponding 1 or 2-day itinerary.

    Inputs:
        all_to_visit: list of tuples - all attractions
        transit_mode: string, "driving" or "transit"
        day: int, 1 or 2

    Output:
        dictionary: key: tuple representing first spot to visit
        value: for 1-day: tuple of ordered route and travel time
                for 2-day: tuple of (day-1 route(ordered),travel time)
                and list of unvisited attractions (unordered)
    '''
    routes = {}  
    for i in range(len(all_to_visit)):
        visited = [all_to_visit[i]]
        to_visit = all_to_visit[:i]+all_to_visit[i+1:]
        
        if day == 1:    
            routes[visited[0]] = single_day_route(visited, to_visit, transit_mode)
        else:
            routes[visited[0]] = first_day_route(visited, to_visit, transit_mode)
    return routes


def route_from_locations(loc_lst, LOCATIONS, all_to_visit, routes, transit_mode, day=1):
    '''
    Given a location (hotel/airbnb), decide the recommended 1/2-day route
    and calculate the total time spent on travel.

    Inputs:
        loc_lst: list of index from LOCATIONS dataframe
        LOCATIONS: dataframe
        all_to_visit: list of tuples - all attractions
        routes: dictionary returned from function "possible_routes"
        transit_mode: string, "driving" or "transit"
        day: int, 1 or 2

    Output:
        dictionary: key - index of location
        value: dictionary {"day 1 route" or "route": list of tuples,
        (if applicable) "day 2 route": list of tuples,
        "total travel time": int}
    '''
    travel_info = {}
    for location in loc_lst:
        d = {}
        (next_spot, to_visit), t_init = decide_next_spot(location, all_to_visit,
            LOCATIONS, ATTRACTIONS, transit_mode)
        route = routes[next_spot]
        
        if day == 1:
            d["route"] = route[0]
            t_end = transit_time(route[0][-1][0], location,
                ATTRACTIONS, LOCATIONS, transit_mode)
            d["total travel time"] = t_init + route[1] + t_end    

        else:
            #Day 1
            d["day 1 route"] = route[0][0]
            t_end = transit_time(route[0][0][-1][0],
                location, ATTRACTIONS, LOCATIONS, transit_mode)
            day_one_t = t_init + route[0][1] + t_end
            
            #Day 2
            day_two_to_visit = route[1]
            (next_spot_2, to_visit_2), t_init_2 = decide_next_spot(location,
                day_two_to_visit, LOCATIONS, ATTRACTIONS, transit_mode)
            route_2, t_2 = single_day_route([next_spot_2], to_visit_2, transit_mode)
            d["day 2 route"] = route_2
            t_end_2 = transit_time(route_2[-1][0], location,
                ATTRACTIONS, LOCATIONS, transit_mode)
            day_two_t = t_init_2 + t_2 + t_end_2
    
            d["total travel time"] = day_one_t + day_two_t
        travel_info[location] = d
    
    return travel_info

def filter_output(output, n): # for flexibility, mean+n*sd
    '''
    '''
    t_l = []
    filter_l = []
    filter_output = {}
    for key in output:
        t = output[key]["total travel time"]       
        t_l += [t]
    t_mean = statistics.mean(t_l)
    t_sd = statistics.stdev(t_l)
    t_benchmark = t_mean - n*t_sd
    for key in output:
        t = output[key]["total travel time"]
        if t <= t_benchmark:
            filter_l += [key]
    for i in filter_l:
        filter_output[i] = output[i]
        
    return (filter_output) 

def select_by_routes(prefs, LOCATIONS, day, transit_mode, n=0):
    '''

    '''
    all_to_visit = select_attraction(ATTRACTIONS, prefs, day)
    routes = possible_routes(all_to_visit, transit_mode, day)
    d = route_from_locations(range(len(LOCATIONS)), LOCATIONS, all_to_visit, routes, transit_mode, day)
    output = filter_output(d, n)
    return output