import numpy as np
import random
from itertools import permutations
from scipy.spatial import distance_matrix

class TravellingThief:
    def __init__(self, population_size, dimension, num_items, capacity, min_speed, max_speed, renting_ratio, edge_weight_type):
        self.population_size = population_size
        self.dimension = dimension
        self.num_items = num_items
        self.capacity = capacity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.renting_ratio = renting_ratio
        self.edge_weight_type = edge_weight_type
        self.distance_matrix = None
        self.profit_table = None

    def parse_input(self, node_coord, profit_matrix):
        # Assuming node_coord and profit_matrix are DataFrames
        self.distance_matrix = self.calculate_distance_matrix(node_coord)
        self.profit_table = profit_matrix

    def calculate_distance_matrix(self, node_coord):
        coordinates = node_coord[['X', 'Y']].values
        return distance_matrix(coordinates, coordinates)

    def generate_solutions(self):
        tsp_solutions = list(permutations(range(1, self.dimension + 1)))
        knapsack_solutions = list(permutations([0, 1], self.num_items))

        # Randomly select population_size solutions
        tsp_population = [list(np.random.choice(sol)) for sol in np.random.choice(tsp_solutions, self.population_size)]
        knapsack_population = [list(np.random.choice(sol)) for sol in np.random.choice(knapsack_solutions, self.population_size)]

        return tsp_population, knapsack_population
