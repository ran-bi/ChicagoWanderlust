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