import pandas as pd
import numpy as np
import random
attractions = pd.read_csv('Attraction List.csv', index_col = 'Identifier')

def select_attraction(df, pref1=None, pref2=None, pref3=None, day=1):   
    if day == 1:
        threshold = (6, 8)  #[6,8]
    else:
        threshold = (12, 15)  #[12,15]
        
    prefs = []
    sum_hours = 0
    selected = []
  
    if pref1 is not None:
        prefs.append([df[pref1] == 1, df[pref1] == 0])
        
        if pref2 is not None:
            prefs.append([df[pref2] == 1, df[pref2] == 0])
        
            if pref3 is not None:
                prefs.append([df[pref3] == 1, df[pref3] == 0])
    
    pref_n = len(prefs)
    
    criteria = [[[0],[1]],[(0,0),(0,1),(1,0),(1,1)],
                [(0,0,0),(0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1)]]
    
    for i in range(2**pref_n):
        if pref_n == 0:
            df_select = df
        else:
            c = criteria[pref_n-1][i]
            select = prefs[0][c[0]]
            for j in range(1, pref_n):
                select = select & prefs[j][c[j]]
            df_select = df[select]
                        
        for row in df_select.itertuples():
            sum_hours += row[2]
            if sum_hours > threshold[1]:
                sum_hours -= row[2]
                if sum_hours < threshold[0]:
                    continue
                return selected
            selected.append((row[0], row[2]))
            print(row[1])

            
###to be replaced

def dummy(i, j):
    random.seed(j)
    return random.randint(1,30)


#input: list of tuples
#recursion

def decide_next_spot(start_point, to_visit):
    next_ = 0
    min_ = dummy(start_point, to_visit[next_][0])
    for i in range(1, len(to_visit)):
        time = dummy(start_point, to_visit[i][0])
        if time < min_:
            min_ = time
            next_ = i
    next_spot = to_visit[next_]
    del to_visit[next_]
    
    return [(next_spot, to_visit), min_]


def single_day_route(visited, to_visit, travel_t = 0):  
    if len(to_visit) == 0:
        return visited+to_visit, travel_t
    
    [(next_spot, to_visit), t] = decide_next_spot(visited[-1][0], to_visit)
    visited.append(next_spot)
    travel_t += t
    
    return single_day_route(visited, to_visit, travel_t)


def first_day_route(visited, to_visit, sum_hours = 0, travel_t = 0, popped = None):
    if popped is None:
        popped = []
        
    if sum_hours > 8:
        place = visited.pop()
        popped.append(place)
        sum_hours -= place[1]
       
        if sum_hours >= 6:
            return (visited, travel_t), to_visit+popped
    
    if len(visited) == 1:
        sum_hours = visited[0][1]
        
    [(next_spot, to_visit), t] = decide_next_spot(visited[-1][0], to_visit)
    sum_hours += next_spot[1]
    visited.append(next_spot)
    travel_t += t

    return first_day_route(visited, to_visit, sum_hours, travel_t, popped)


def start_place_and_routes(all_to_visit, day=1):
    routes = {}
    
    for i in range(len(all_to_visit)):
        visited = [all_to_visit[i]]
        to_visit = all_to_visit[:i]+all_to_visit[i+1:]
        
        if day == 1:    
            route = single_day_route(visited, to_visit)
            routes[visited[0]] = route
        else:
            day_one_route, day_two_to_visit = first_day_route(visited, to_visit)
            routes[visited[0]] = [day_one_route, day_two_to_visit]
    
    return routes


def route_from_hotels(locations, all_to_visit, routes, day=1):
    travel_info = {}
    for location in locations:
        d = {}
        [(next_spot, to_visit), t_init] = decide_next_spot(location, all_to_visit)
        route = routes[next_spot]
        
        if day == 1:
            d["route"] = route[0]
            t_end = dummy(route[0][-1][0], location)
            d["total travel time"] = t_init + route[1] + t_end    

        else:
            #Day 1
            d["day 1 route"] = route[0][0]
            t_end = dummy(route[0][0][-1][0], location)
            day_one_t = t_init + route[0][1] + t_end
            #Day 2
            day_two_to_visit = route[1]
            [(next_spot_2, to_visit_2), t_init_2] = decide_next_spot(location, day_two_to_visit)
            route_2, t_2 = single_day_route([next_spot_2], day_two_to_visit)
            d["day 2 route"] = route_2
            t_end_2 = dummy(route_2[-1][0], location)
            day_two_t = t_init_2 + t_2 + t_end_2
            
            d["total travel time"] = day_one_t + day_two_t
        
        travel_info[location] = d
    return travel_info


  