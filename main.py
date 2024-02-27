# additional files
import definition as d

# parameters
problem = "input/a280.txt"
num_of_generation = 10000
m = None   # number of cities

n = 150    # number of people in population
s = 3      # parameter for selection
pc = 0.7   # parameter for crossover
pm = 0.2  # parameter for mutation

# algorithm body
distance_matrix = d.distance_matrix(problem)
m = len(distance_matrix)

pop_P = d.new_population(n, m)
fitness = d.evaluate_population(pop_P, distance_matrix)

best_index = d.find_best_individual_index(fitness)
best_ind = (pop_P[best_index][:], fitness[best_index])

print(best_ind[1])
best_results = [best_ind[1]]
best_in_pop = [best_ind[1]]
avg_pop = [sum(fitness)/len(fitness)]
worst_pop = [max(fitness)]

for i in range(num_of_generation):
    pop_T = d.tournament_selection(pop_P, fitness, s)

    pop_O = d.crossover(pop_T, pc)

    d.mutation(pop_O, pm)

    fitness = d.evaluate_population(pop_O, distance_matrix)

    best_index = d.find_best_individual_index(fitness)
    if fitness[best_index] < best_ind[1]:
        best_ind = (pop_O[best_index][:], fitness[best_index])  # spr. czy [:] jest potrzebna
    best_results.append(best_ind[1])
    best_in_pop.append(fitness[best_index])
    avg_pop.append(sum(fitness)/len(fitness))
    worst_pop.append(max(fitness))

    pop_P = pop_O

    if i % 100 == 0:
        print(best_ind[1])

# best result
print()
d.print_individual(best_ind[0], best_ind[1])
