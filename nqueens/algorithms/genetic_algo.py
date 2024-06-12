import random

def genetic_algorithm(nqueens):
    population_size = 1000
    mutation_rate = 0.5
    max_generations = 1000

    def generate_individual():
        return [random.randint(0, nqueens.N - 1) for _ in range(nqueens.N)]

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, nqueens.N - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent1[crossover_point:] + parent2[:crossover_point]
        return child1, child2

    def mutate(individual):
        if random.random() < mutation_rate:
            individual[random.randint(0, nqueens.N - 1)] = random.randint(0, nqueens.N - 1)
        return individual

    population = [generate_individual() for _ in range(population_size)]
    for generation in range(max_generations):
        population = sorted(population, key=lambda x: sum(nqueens.calculate_attacks(x)))
        if sum(nqueens.calculate_attacks(population[0])) == 0:
            nqueens.board = population[0]
            return population_size, max_generations, mutation_rate, True
        next_generation = population[:10]
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1))
            next_generation.append(mutate(child2))
        population = next_generation[:]
    nqueens.board = population[0]
    return population_size, max_generations, mutation_rate, False