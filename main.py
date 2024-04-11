# additional files
import functions as f

# parameters
problem = "input/pr107.txt"
num_of_generation = 10000
m = None                    # number of cities
n = 500                     # number of people in population
s = 3                       # parameter for selection
pc = 0.8                    # parameter for crossover
pm = 0.3                    # parameter for mutation
# crossover_v = 'pmx'         # options: 'pmx'
mutation_v = 'inversion'    # options: 'inversion', 'exchange', 'inversion_complex'

# creating instance for distance matrix
matrix = f.Matrix()

# distance matrix calculation
distance_matrix = matrix.distance(problem)
m = len(distance_matrix)

# creating instances for classes
crossover = f.Crossover()
mutation = f.Mutation()
population = f.Population(m=m, n=n)
fitness = f.Fitness(distance_matrix)
selection = f.Selection()

pop_P = population.new_population()
fit = fitness.evaluate_population(pop_P)

best_index = fitness.find_best_individual_index(fit)
best_ind = (pop_P[best_index][:], fit[best_index])

print(best_ind[1])
best_results = [best_ind[1]]
best_in_pop = [best_ind[1]]
avg_pop = [sum(fit)/len(fit)]
worst_pop = [max(fit)]

for i in range(num_of_generation):
    pop_T = selection.tournament(pop_P, fit, s)

    pop_O = crossover.execute(pop_T, pc)

    mutation.execute(pop_O, pm, mutation_v)

    fit = fitness.evaluate_population(pop_O)

    best_index = fitness.find_best_individual_index(fit)
    if fit[best_index] < best_ind[1]:
        best_ind = (pop_O[best_index][:], fit[best_index])
    best_results.append(best_ind[1])
    best_in_pop.append(fit[best_index])
    avg_pop.append(sum(fit)/len(fit))
    worst_pop.append(max(fit))

    pop_P = pop_O

    if i % 1000 == 0:
        print(best_ind[1])

# best result
print()
population.print_ind(best_ind[0], best_ind[1])
