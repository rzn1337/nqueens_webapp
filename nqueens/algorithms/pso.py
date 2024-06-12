import random
import math


class Particle:
    def __init__(self, nqueens):
        self.position = [random.randint(0, nqueens.N - 1) for _ in range(nqueens.N)]
        self.velocity = [random.uniform(-1, 1) for _ in range(nqueens.N)]
        self.best_position = self.position[:]
        self.best_attacks = sum(nqueens.calculate_attacks(self.position))


def particle_swarm_optimization(nqueens,
                                num_particles=300,
                                max_iterations=10000,
                                inertia_weight=0.729, # greater the inertia higher the exploration and vice versa
                                cognitive_weight=1.49445,
                                social_weight=1.49445):

    particles = [Particle(nqueens) for _ in range(num_particles)] # assign random config to each particle
    global_best_position = None
    global_best_attacks = float('inf')

    for iteration in range(max_iterations):
        for particle in particles:
            current_attacks = sum(nqueens.calculate_attacks(particle.position)) # calculate fitness for each config/particle

            if current_attacks < particle.best_attacks:     # update particle's best config --> least fitness score
                particle.best_attacks = current_attacks
                particle.best_position = particle.position[:]

            if current_attacks < global_best_attacks:       # update global best config --> least fitness score
                global_best_attacks = current_attacks
                global_best_position = particle.position[:]

        if global_best_attacks == 0:
            break

        for particle in particles:
            for i in range(nqueens.N):                              # calculate new position for each queen in a particle
                r1, r2 = random.random(), random.random()
                cognitive_velocity = cognitive_weight * r1 * (particle.best_position[i] - particle.position[i])
                social_velocity = social_weight * r2 * (global_best_position[i] - particle.position[i])
                particle.velocity[i] = inertia_weight * particle.velocity[i] + cognitive_velocity + social_velocity
                particle.position[i] = min(max(int(particle.position[i] + particle.velocity[i]), 0), nqueens.N - 1)
    #end loop (go back up)
    nqueens.board = global_best_position
    return num_particles, max_iterations, inertia_weight, cognitive_weight, social_weight, global_best_attacks == 0