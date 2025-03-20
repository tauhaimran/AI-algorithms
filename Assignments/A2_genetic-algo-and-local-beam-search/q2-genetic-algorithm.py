# tauha imran 22i1239 cs-g AI A2 q2
import random

# Product and shelf constraints
shelves = {
    "S1": {'capacity': 8, 'type': "checkout"},
    "S2": {'capacity': 25, 'type': "lower"},
    "S4": {'capacity': 15, 'type': "eye-level"},
    "S5": {'capacity': 20, 'type': "general"},
    "R1": {'capacity': 20, 'type': "refrigerated"},
    "H1": {'capacity': 10, 'type': "hazardous"}
}

products = {
    "P1": {'weight': 5, 'category': "dairy", 'requirement': "refrigerated"},
    "P2": {'weight': 10, 'category': "grains", 'requirement': None},
    "P3": {'weight': 5, 'category': "frozen", 'requirement': "refrigerated"},
    "P4": {'weight': 3, 'category': "cereal", 'requirement': None},
    "P5": {'weight': 2, 'category': "pasta", 'requirement': None},
    "P6": {'weight': 3, 'category': "sauce", 'requirement': None},
    "P7": {'weight': 4, 'category': "detergent", 'requirement': "hazardous"},
    "P8": {'weight': 5, 'category': "cleaning", 'requirement': "hazardous"}
}

product_info = {product_id: {'name': product_info['category'], 'weight': product_info['weight']} for product_id, product_info in products.items()}

# Fitness function

def fitness(individual):
    shelf_loads = {shelf: 0 for shelf in shelves.keys()}
    penalty = 0

    for product, shelf in individual.items():
        if shelf not in shelves:
            penalty += 100  # Invalid shelf assignment
        else:
            product_info = products[product]
            shelf_info = shelves[shelf]

            shelf_loads[shelf] += product_info['weight']

            if product_info['requirement'] and product_info['requirement'] != shelf_info['type']:
                penalty += 50  # Wrong placement

    # Overloaded shelves
    for shelf, load in shelf_loads.items():
        if load > shelves[shelf]['capacity']:
            penalty += (load - shelves[shelf]['capacity']) * 10

    return -penalty  # Lower penalty is better


# Generate initial population

def generate_population(size):
    population = []
    shelf_ids = list(shelves.keys())

    for _ in range(size):
        individual = {product: random.choice(shelf_ids) for product in products}
        population.append(individual)

    return population


# Crossover operation

def crossover(parent1, parent2):
    all_products = list(products.keys())
    split_point = random.randint(0, len(all_products) - 1)
    child = {}

    for product in all_products[:split_point]:
        child[product] = parent1[product]
    for product in all_products[split_point:]:
        child[product] = parent2[product]

    return child


# Mutation operation

def mutate(individual, mutation_rate=0.1):
    shelf_ids = list(shelves.keys())

    for product in individual:
        if random.random() < mutation_rate:
            individual[product] = random.choice(shelf_ids)

    return individual


# Genetic Algorithm

def genetic_algorithm(pop_size=10, generations=50, mutation_rate=0.1):
    population = generate_population(pop_size)

    for _ in range(generations):
        population = sorted(population, key=fitness, reverse=True)[:pop_size]
        new_population = population[:2]  # Elitism

        while len(new_population) < pop_size:
            parents = random.sample(population, 2)
            child = mutate(crossover(parents[0], parents[1]), mutation_rate)
            new_population.append(child)

        population = new_population

    return max(population, key=fitness)


# driver code to run the GA
best_solution = genetic_algorithm()

shelf_details = {shelf: {'products': [], 'total_weight': 0, 'capacity': shelves[shelf]['capacity']} for shelf in shelves}

for product, shelf in best_solution.items():
    shelf_details[shelf]['products'].append(product)
    shelf_details[shelf]['total_weight'] += products[product]['weight']

# Display results
for shelf, details in shelf_details.items():
    print(f"\nShelf {shelf}:")
    print(f"  Max Weight Allowed: {details['capacity']} kg")
    print(f"  Total Weight Placed: {details['total_weight']} kg")
    
    # Get product names instead of IDs
    product_names = [product_info[product_id]['name'] for product_id in details['products']]  
    print(f"  Products: {', '.join(product_names) if product_names else 'None'}") 

print("\nFitness of solution:", fitness(best_solution))
