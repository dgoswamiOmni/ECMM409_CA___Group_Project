import concurrent.futures
import pandas as pd
import numpy as np

def parse_variables(lines):
    variables = {}
    for line in lines:
        if line.startswith("PROBLEM NAME:"):
            variables['problem_name'] = line.split(':')[1].strip()
        elif line.startswith("KNAPSACK DATA TYPE:"):
            variables['knapsack_data_type'] = line.split(':')[1].strip()
        elif line.startswith("DIMENSION:"):
            variables['dimension'] = int(line.split(':')[1].strip())
        elif line.startswith("NUMBER OF ITEMS:"):
            variables['num_items'] = int(line.split(':')[1].strip())
        elif line.startswith("CAPACITY OF KNAPSACK:"):
            variables['knapsack_capacity'] = int(line.split(':')[1].strip())
        elif line.startswith("MIN SPEED:"):
            variables['min_speed'] = float(line.split(':')[1].strip())
        elif line.startswith("MAX SPEED:"):
            variables['max_speed'] = float(line.split(':')[1].strip())
        elif line.startswith("RENTING RATIO:"):
            variables['renting_ratio'] = float(line.split(':')[1].strip())
        elif line.startswith("EDGE_WEIGHT_TYPE:"):
            variables['edge_weight_type'] = line.split(':')[1].strip()
    return variables
def parse_node_coord(lines, start_line, dimension):
    data = []
    for line in lines[start_line:start_line + dimension]:
        parts = line.split()
        index = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        data.append({'Index': index, 'X': x, 'Y': y})
    return pd.DataFrame(data)

def parse_item_section(lines, start_line, dimension):
    data = []
    for line in lines[start_line:start_line + dimension]:
        index, profit, weight, assigned_node = map(int, line.split())
        data.append({'Index': index, 'Profit': profit, 'Weight': weight, 'Assigned_Node': assigned_node})
    return pd.DataFrame(data)

def parse_file_parallel(lines, dimension):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_node_coord = executor.submit(parse_node_coord, lines, 10, dimension)
        future_profit_matrix = executor.submit(parse_item_section, lines, 10 + dimension + 1, dimension)

    node_coord = future_node_coord.result()
    profit_matrix = future_profit_matrix.result()

    return node_coord, profit_matrix


# Example usage:

with open('/Users/devarshigoswami/Desktop/work/nature_inspired_computation/TravellingThief/gecco19-thief/ECMM409_CA___Group_Project/test-example-n4.txt', 'r') as file:
    lines = file.readlines()

variables = parse_variables(lines)
node_coord, profit_matrix = parse_file_parallel(lines, variables['dimension'])

print("Variables:", variables)
print("Node Coord:", node_coord)
print("Profit Matrix:", profit_matrix)

profit_table=profit_matrix.copy()

def calculate_distance_matrix(node_coord):
    coordinates = node_coord[['X', 'Y']].values
    x, y = np.meshgrid(coordinates[:, 0], coordinates[:, 1])

    distance_matrix = np.sqrt((x - x.T)**2 + (y - y.T)**2)
    
    return distance_matrix

distance_matrix=calculate_distance_matrix(node_coord)

tour_example=[1,3,2,4]
packing_plan_example=[1,0,1]
profit_table['Picked'] = packing_plan_example


def calculate_current_velocity(weight, capacity, min_speed, max_speed):
    if weight <= capacity:
        return max_speed - (weight / capacity) * (max_speed - min_speed)
    else:
        return min_speed

# def calculate_cost(tour, packing_plan, variables,distance_matrix,profit_table):
#     dimension = variables['dimension']
#     max_speed = variables['max_speed']

#     current_weight = 0
#     total_time = 0
#     current_velocity = max_speed

#     for i in range(dimension):
#         # Calculate the distance between consecutive cities
#         distance = distance_matrix[tour[(i % dimension)]-1][tour[(i + 1) % dimension]-1]

#         # Calculate the time taken to travel the distance
#         time_to_travel = distance / current_velocity
#         total_time += time_to_travel

#         # Update current weight based on the packing plan
#         current_weight += (profit_table[profit_table['Assigned_Node']==tour[i+1]]['Weight']*profit_table[profit_table['Assigned_Node']==tour[i+1]]['Picked']).values[0]
#         # Calculate the current velocity
#         current_velocity = calculate_current_velocity(current_weight, variables['knapsack_capacity'],variables['min_speed'], variables['max_speed'])
#         print(i,current_weight,current_velocity,distance,time_to_travel)

#     return total_time

# print(calculate_cost(tour=tour_example,packing_plan=packing_plan_example,variables=variables,distance_matrix=distance_matrix,profit_table=profit_table))


def calculate_cost(tour, packing_plan, variables, distance_matrix, profit_table):
    dimension = variables['dimension']
    max_speed = variables['max_speed']

    total_time = 0
    current_velocity = max_speed
    current_weight = 0

    for i in range(dimension):
        # Calculate the distance between consecutive cities
        from_city = tour[i]
        to_city = tour[(i + 1) % dimension]
        distance = distance_matrix[from_city - 1][to_city - 1]

        # Calculate the time taken to travel the distance
        time_to_travel = distance / current_velocity

        # Explain the current step
        print(f"At city {from_city}:")
        print(f"  Knapsack weight before picking: {current_weight}")
        print(f"  Current velocity: {current_velocity}")
        print(f"  Distance to next city ({to_city}): {distance}")
        print(f"  Time to travel: {time_to_travel}")

        if i < len(packing_plan):
            # Update current weight based on the packing plan
            picked_item_weight = (profit_table[(profit_table['Assigned_Node'] == to_city)]['Weight']*profit_table[(profit_table['Assigned_Node'] == to_city)]['Picked']).values[0]
            # current_weight += picked_item_weight * packing_plan[i]
            print(f"  Knapsack weight after picking item {i + 1}: {current_weight}")

        # Calculate the current velocity
        current_velocity = calculate_current_velocity(current_weight, variables['knapsack_capacity'], variables['min_speed'], variables['max_speed'])
        print(f"  Updated velocity: {current_velocity}")

        # Accumulate the time taken for this step
        total_time += time_to_travel

    print(f"Total traveling time: {total_time}")
    return total_time

# Example usage:
print(calculate_cost(tour=tour_example, packing_plan=packing_plan_example, variables=variables, distance_matrix=distance_matrix, profit_table=profit_table))
