import random
import math

class Ant:
    def __init__(self, nqueens):
        self.nqueens = nqueens
        self.path = []
        self.attacks = []

    def add_queen(self, col):
        self.path.append(col)
        self.attacks = self.nqueens.calculate_attacks(self.path)

    def reset(self):
        self.path = []
        self.attacks = []

def ant_colony_optimization(nqueens, num_ants=100, num_iterations=1000, alpha=1, beta=2, evaporation_rate=0.01, pheromone_constant=100.0):
    pheromone = [[1 for _ in range(nqueens.N)] for _ in range(nqueens.N)]
    best_solution = None
    best_attacks = float('inf')

    for iteration in range(num_iterations):
        ants = [Ant(nqueens) for _ in range(num_ants)]

        for ant in ants:
            for row in range(nqueens.N):
                probabilities = [
                    ((pheromone[row][col] ** alpha) * ((1.0 / (1 + sum(nqueens.calculate_attacks(ant.path + [col])))) ** beta))
                    for col in range(nqueens.N)
                ]
                total = sum(probabilities)
                probabilities = [p / total for p in probabilities]
                col = random.choices(range(nqueens.N), probabilities)[0]
                ant.add_queen(col)

            current_attacks = sum(ant.attacks)
            if current_attacks < best_attacks:
                best_attacks = current_attacks
                best_solution = ant.path[:]

        if best_attacks == 0: 
            break

        for ant in ants:
            for row in range(nqueens.N):
                pheromone[row][ant.path[row]] += pheromone_constant / best_attacks

        for row in range(nqueens.N):
            for col in range(nqueens.N):
                pheromone[row][col] *= (1 - evaporation_rate)

    if best_solution:
        nqueens.board = best_solution
        return num_ants, num_iterations, alpha, beta, evaporation_rate, pheromone_constant, sum(nqueens.calculate_attacks(best_solution)) == 0
    return num_ants, num_iterations, alpha, beta, evaporation_rate, pheromone_constant, False