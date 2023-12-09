import concurrent.futures
import pandas as pd
import numpy as np


def parse_node_coord(lines, start_line, dimension):
    data = []
    for line in lines[start_line:start_line + dimension]:
        index, x, y = map(int, line.split())
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

with open('a280-n279.txt', 'r') as file:
    lines = file.readlines()

variables = parse_variables(lines)
node_coord, profit_matrix = parse_file_parallel(lines, variables['dimension'])

print("Variables:", variables)
print("Node Coord:", node_coord)
print("Profit Matrix:", profit_matrix)

def calculate_distance_matrix(node_coord):
    coordinates = node_coord[['X', 'Y']].values
    x, y = np.meshgrid(coordinates[:, 0], coordinates[:, 1])

    distance_matrix = np.sqrt((x - x.T)**2 + (y - y.T)**2)
    
    return distance_matrix
