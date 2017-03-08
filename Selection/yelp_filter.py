import rauth
import statistics
# import ast

# output sample
'''
output = {8: {'total travel time': 181, 'day 1 route': [(29, 1.0), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (24, 1.25), (2, 1.75), (20, 1.25)]}, \
1: {'total travel time': 167, 'day 1 route': [(17, 4.0), (8, 2.0)], 'day 2 route': [(13, 2.5), (12, 1.25), (29, 1.0), (24, 1.25), (2, 1.75), (20, 1.25)]}, \
20: {'total travel time': 223, 'day 1 route': [(24, 1.25), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (29, 1.0), (2, 1.75), (20, 1.25)]}, \
 39: {'total travel time': 179, 'day 1 route': [(2, 1.75), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (29, 1.0), (24, 1.25), (20, 1.25)]}}
'''
# params["limit"]
def get_search_parameters(lat,lon):
    #See the Yelp API for more details
    params = {}
    params["term"] = "restaurant"
    params["ll"] = "{},{}".format(str(lat),str(lon))
    params["radius_filter"] = "2000"
    params["limit"] = "10" #Yelp will only return a max of 40 results at a time

    return params


def get_results(params):

    #Obtain these from Yelp's manage access page
    consumer_key = "yk-sQRKSX0mitrxx6VMN_g"
    consumer_secret = "L0Q9YXv0KT27XpJ3jQNkL2qCaZY"
    token = "4HL--_tknW9UyCSJL8xRGOm0ZP8b2J4p"
    token_secret = "tzfwqT1NUaGKQzuAdiatEHH4nWc"
    
    session = rauth.OAuth1Session(
        consumer_key = consumer_key
        ,consumer_secret = consumer_secret
        ,access_token = token
        ,access_token_secret = token_secret)
        
    request = session.get("http://api.yelp.com/v2/search",params=params)
    
    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()
    
    return data

# limit_num
def get_food_index(index,df_location):
    lat, lon = df_location.loc[index][0]
    # lat, lon = ast.literal_eval(df_location.loc[index][0])
    restaurant_dic = get_results(get_search_parameters(lat,lon))
    if 'businesses' not in restaurant_dic:
        return None
    else:
        limit_num = 10
        l = []
        for i in range(limit_num):

                rating = restaurant_dic['businesses'][i]['rating']
                review_count = restaurant_dic['businesses'][i]['review_count']
                a = [(rating, review_count)]
                l = l + a

        rating_l = []
        review_count_l = []
        for i in l:
            rating, review_count = i
            rating_l += [rating]
            review_count_l += [review_count]
        rating = statistics.mean(rating_l)
        review = statistics.mean(review_count_l)

        return (rating,review)

def get_mean_sd(output, df_location, n): # for flexibility, mean+n*sd
    rating_l = []
    review_l = []
    for key in output:
        rv = get_food_index(key, df_location)
        if rv:
            rating, review = rv
            rating_l += [rating]
            review_l += [review]

    rating_mean = statistics.mean(rating_l)
    review_mean = statistics.mean(review_l)
    rating_sd = statistics.stdev(rating_l)
    review_sd = statistics.stdev(review_l)
    return (rating_mean+n*rating_sd, review_mean+n*review_sd)

def get_filter_l(output, df_location, n): # for flexibility, mean+n*sd
    filter_l = []
    for key in output:
        print(key)
        rv = get_food_index(key, df_location)
        if rv:
            rating, review = rv
            rating_benchmark, review_benchmark = get_mean_sd(output, df_location, n)
            if rating >= rating_benchmark and review >= review_benchmark:
                filter_l += [key]
    return filter_l


#a['businesses'][0]['rating']
#a['businesses'][0]['review_count']
#a['businesses'][1]['review_count']
