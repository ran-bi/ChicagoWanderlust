import statistics


# output sample
output = {8: {'total travel time': 181, 'day 1 route': [(29, 1.0), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (24, 1.25), (2, 1.75), (20, 1.25)]}, \
1: {'total travel time': 167, 'day 1 route': [(17, 4.0), (8, 2.0)], 'day 2 route': [(13, 2.5), (12, 1.25), (29, 1.0), (24, 1.25), (2, 1.75), (20, 1.25)]}, \
20: {'total travel time': 223, 'day 1 route': [(24, 1.25), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (29, 1.0), (2, 1.75), (20, 1.25)]}, \
39: {'total travel time': 179, 'day 1 route': [(2, 1.75), (8, 2.0), (13, 2.5), (12, 1.25)], 'day 2 route': [(17, 4.0), (29, 1.0), (24, 1.25), (20, 1.25)]}}

def filter_output(output, n): # for flexibility, mean+n*sd
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
