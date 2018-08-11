#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

# fetch input_data
####
# file_location = 'data/ks_19_0'
# with open(file_location, 'r') as input_data_file:
#     input_data = input_data_file.read()
####


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    solutions = {}
    solutions['Dynamic Programming'] = {}
    solutions['Dynamic Programming']['value'] = 0
    solutions['Dynamic Programming']['weight'] = 0
    solutions['Dynamic Programming']['taken'] = [0]*len(items)

######## Using Dynamic Programming ############

    cost_function = {}

    for caps in range(capacity+1):
        cost_function[-1, caps] = 0

    for caps in range(capacity+1):
        for k in range(item_count):
            if items[k].weight > caps:
                cost_function[k, caps] = cost_function[k-1, caps]
            elif items[k].weight <= caps:
                cost_function[k, caps] = max(items[k].value +
                                             cost_function[k-1,
                                             caps-items[k].weight],
                                             cost_function[k-1, caps])

    # The maximum cost value would be the last value added as we are doing
    # it dynamically

    f_max = cost_function[item_count-1, capacity-1]

    # Backtracking for the solution

    temp_capacity = capacity

    for k in range(item_count-1, -1, -1):
        for cap in range(temp_capacity, 0, -1):
            if cost_function[k, cap] == cost_function[k-1, cap]:
                solutions['Dynamic Programming']['taken'][k] = 0
            else:
                solutions['Dynamic Programming']['taken'][k] = 1
                solutions['Dynamic Programming']['value'] += items[k].value
                temp_capacity = temp_capacity - items[k].weight
                break




######## Using weight desnsity heuristic ########

    solutions['Weight Density'] = {}
    solutions['Weight Density']['value'] = 0
    solutions['Weight Density']['weight'] = 0
    solutions['Weight Density']['taken'] = [0]*len(items)
    #
    weight_density = [(item.index, item.value/item.weight) for item in items]
    weight_density = sorted(weight_density, key= lambda x: x[1], reverse=True)

    for item in weight_density:
        if solutions['Weight Density']['weight'] + items[item[0]].weight <= capacity:
            solutions['Weight Density']['taken'][item[0]] = 1
            solutions['Weight Density']['value'] += items[item[0]].value
            solutions['Weight Density']['weight'] += items[item[0]].weight


######## Choosing the best solution #########

    if solutions['Weight Density']['value'] >= solutions['Dynamic Programming']['value']:
        for i, j in solutions['Weight Density'].items():
            exec('%s=%s' % (i, j), globals())
    else:
        for i, j in solutions['Dynamic Programming'].items():
            exec('%s=%s' % (i, j), globals())

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
