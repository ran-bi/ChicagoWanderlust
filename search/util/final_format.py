def get_route(location_index, output, df_spots):

    if 'route' in output[location_index]:
        route_l = []
        spots_l = output[location_index]['route']
        for j in spots_l:
            spot_index, t = j
            spot_str = df_spots.loc[spot_index]['Attraction Name']
            route_l += [spot_str]
            route_str = ' --> '.join(route_l)
    else:
        route_l1 = []
        spots_l1 = output[location_index]['day 1 route']
        for j in spots_l1:
            spot_index, t = j
            spot_str = df_spots.loc[spot_index]['Attraction Name']
            route_l1 += [spot_str]
            route_str1 = ' --> '.join(route_l1)

        route_l2 = []
        spots_l2 = output[location_index]['day 2 route']
        for j in spots_l2:
            spot_index, t = j
            spot_str = df_spots.loc[spot_index]['Attraction Name']
            route_l2 += [spot_str]
            route_str2 = ' --> '.join(route_l2)

        route_str = '#Day 1 ' + route_str1 + "   " + '#Day 2 ' + route_str2

    return route_str

def get_final_output(index_list, output, df_spots, df_location):
    l = len(index_list)
    final_output = {}
    for i in range(l):
        final_output["Hotel"+str(i+1)] = df_location.loc[index_list[i]]['name']
        final_output['Price'+str(i+1)] = df_location.loc[index_list[i]]['price']
        final_output['BookingLink'+str(i+1)] = df_location.loc[index_list[i]]['url']
        final_output['Coord'+str(i+1)] = df_location.loc[index_list[i]]['coord']
        final_output['Route'+str(i+1)] = get_route(index_list[i], output, df_spots)

    if l < 5:
        for i in range(l+1, 6):
            final_output["Hotel"+str(i)] = ''
            final_output['Price'+str(i)] = ''
            final_output['BookingLink'+str(i)] = ''
            final_output['Coord'+str(i)] = ''
            final_output['Route'+str(i)] = ''

    return final_output




