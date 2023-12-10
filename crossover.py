import random

def biased_crossover(elite_parent, non_elite_parent, rho_e):
    # Ensure both parents have the same length
    assert len(elite_parent) == len(non_elite_parent)

    offspring = []

    for i in range(len(elite_parent)):
        # Generate a random number between 0 and 1
        rand_value = random.random()

        # Determine whether to inherit from the elite parent or non-elite parent
        if rand_value <= rho_e:
            offspring.append(elite_parent[i])
        else:
            offspring.append(non_elite_parent[i])

    return offspring

# Example usage
elite_solution = [0.2, 0.5, 0.7, 0.3, 0.8, 0.1]
non_elite_solution = [0.2, 0.9, 0.4, 0.6, 0.1, 0.3]
rho_e = 0.7  # Set the bias parameter (adjust as needed)

offspring_solution = biased_crossover(elite_solution, non_elite_solution, rho_e)

print("Offspring Solution:", offspring_solution)
