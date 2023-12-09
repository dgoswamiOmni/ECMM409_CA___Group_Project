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
    
    def has_duplicates(self, sol):
        """ Helper function for fix_duplicates() functions."""
        # Checking if duplicates are present
        duplicates_found = len(sol) != len(set(sol))
        newlist, dupelist = [], []

        # Only runs block if duplicates were found
        if duplicates_found:  
            for i in range(len(sol)):
                if sol[i] not in newlist:
                    # Appending if element has not been seen yet
                    newlist.append(sol[i])
                elif sol[i] in newlist:
                    # Appending if element has already been found
                    dupelist.append(sol[i])
                    
        return dupelist


    def fix_duplicates(self, sol):
        """ Helper function for crossover functions."""
        # All elements that must be included in solution (apart from start_point)
        full_set = set(range(self.dimension))
        
        # Returns any elements that have been duplicated
        duplist = self.has_duplicates(sol)
        
        # Finds any elements that haven't been included in the solution
        missing_elements = list(full_set.difference(set(sol)))
        
        # Performs fix only if duplicated elements were found
        if len(duplist) != 0 :
            for i in range(len(duplist)):
                # Finding index of duplicated element
                ind = sol.index(duplist[i])
                # Replacing the duplicated element
                sol[ind] = missing_elements[i]

        return sol


    def single_crossover(self, tsp_1, tsp_2, k_1, k_2):
        """ Performs the single crossover, by generating a random crossover points
        and combining them as required."""
        # Checking that inputs are valid
        if len(tsp_1) != len(tsp_2) or len(tsp_1) != self.dimension or len(tsp_2) != self.dimension:
            print("Invalid crossover input")
            return
        
        # Generating random crossover point (TSP)
        crossover_point = random.randint(1,self.dimension-1)

        # Creating children based on the generated crossver point
        sol_1 = tsp_1[:crossover_point] + tsp_2[crossover_point:]
        sol_2 = tsp_2[:crossover_point] + tsp_1[crossover_point:]

        # Fixing any duplicated elements in solution
        tsp_child_1 = self.fix_duplicates(sol_1)
        tsp_child_2 = self.fix_duplicates(sol_2)

        # Children for knapsack crossover
        k_child_1 = k_1[:crossover_point] + k_2[crossover_point:]
        k_child_2 = k_2[:crossover_point] + k_1[crossover_point:]

        return tsp_child_1, tsp_child_2, k_child_1, k_child_2


    def multi_crossover(self, tsp_1, tsp_2, k_1, k_2):
        """ Performs the multi crossover, by generating two random crossover points
        and combining them as required."""
        # Checking that inputs are valid
        if len(tsp_1) != len(tsp_2) or len(tsp_1) != self.dimension or len(tsp_2) != self.dimension:
            print("Invalid crossover input")
            return
        
        # Generating two random crossover point (TSP)
        c_point_1 = random.randint(1,self.dimension-1)
        c_point_2 = random.randint(1,self.dimension-1)

        # Creating children based on the generated crossver point
        sol_1 = tsp_1[:c_point_1] + tsp_2[c_point_1:c_point_2] + tsp_1[c_point_2:]
        sol_2 = tsp_2[:c_point_1] + tsp_1[c_point_1:c_point_2] + tsp_2[c_point_2:]

        # Fixing any duplicated elements in solution
        child_1 = self.fix_duplicates(sol_1)
        child_2 = self.fix_duplicates(sol_2)

        # Children from knapsack crossover
        k_child_1 = k_1[:c_point_1] + k_2[c_point_1:c_point_2] + k_1[c_point_2:]
        k_child_2 = k_2[:c_point_1] + k_1[c_point_1:c_point_2] + k_2[c_point_2:]

        return child_1, child_2, k_child_1, k_child_2
    
    

