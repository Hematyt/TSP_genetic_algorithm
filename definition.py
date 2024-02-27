# Libraries
import random


# distance matrix
def distance_matrix(file_name: str):
    file = open(file_name)
    city_num = int(file.readline())
    distance_matrix = [[0 for _ in range(city_num)] for _ in range(city_num)]

    for i_row in range(city_num):
        dist_list = file.readline().split()
        dist_list = list(map(int, dist_list))

        for i_col in range(len(dist_list)):
            distance_matrix[i_row][i_col] = dist_list[i_col]
            distance_matrix[i_col][i_row] = dist_list[i_col]

    file.close()
    return distance_matrix


# population
def new_individual(m: int) -> list:
    ind = list(range(m))
    random.shuffle(ind)
    return ind


def new_population(n: int, m: int) -> list:
    pop = []
    for _ in range(n):
        pop.append(new_individual(m))

    return pop


def print_individual(ind, fit):
    print("-".join(map(str, ind)), fit)


def print_population(pop, fitness=None):
    if not fitness:
        fitness = ["empty" for _ in range(len(pop))]

    for ind, fit in zip(pop, fitness):
        print_individual(ind, fit)


# fitness
def evaluate_individual(ind, dm):
    m = len(ind)
    fit = 0
    for i_gene in range(m-1):  # idziemy do przedostatniego genu
        gene_1 = ind[i_gene]
        gene_2 = ind[i_gene+1]
        fit += dm[gene_1][gene_2]

    # i jeszcze powrót z ostatnigo genu do pierwszego
    gene_1 = ind[-1]
    gene_2 = ind[0]
    fit += dm[gene_1][gene_2]

    return fit


def evaluate_population(pop, dm):
    fitness = []

    for ind in pop:
        eval_ind = evaluate_individual(ind, dm)
        fitness.append(eval_ind)

    return fitness


def find_best_individual_index(fitness):
    # return fitness.index(min(fitness))
    index = 0  # indeks najlepszego (przed pracą np. pierwszego osobnika)
    for i in range(1, len(fitness)):  # przejście przez wszystkie oceny, od drugiego osobnika do końca
        if fitness[i] < fitness[index]:  # jeśli znaleźliśmy lepszy
            index = i
    return index


# selection
def tournament_selection(pop, fitness, k):
    n = len(pop)  # liczba osobników
    new_pop = []

    for _ in range(n):  # Tyle ile jest osobników, tyle mamy turniejów
        best_ind_index = random.randint(0, n-1)

        for _ in range(k-1):  # losujemy jeszcze k-1 osobników, bo pierwszy jest wylosowany w linii 8
            random_ind_index = random.randint(0, n-1)
            if fitness[random_ind_index] < fitness[best_ind_index]:
                best_ind_index = random_ind_index

        new_pop.append(pop[best_ind_index][:])

    return new_pop


# crossover
def fix_pmx(parent, self_mid, second_mid):
    fix = []

    for gene in parent:
        while gene in self_mid:
            pos = self_mid.index(gene)
            gene = second_mid[pos]

        fix.append(gene)

    return fix


def crossover_pmx(parent_1, parent_2):
    m = len(parent_1)

    cut_1 = random.randint(0, m)
    cut_2 = random.randint(cut_1+1, m+1)
    cut_2 += 1  # bo chcemy dopuścić sytuację, że nie ma suffix

    child_1_middle = parent_1[cut_1:cut_2]
    child_2_middle = parent_2[cut_1:cut_2]

    child_1_prefix = fix_pmx(parent_2[:cut_1], child_1_middle, child_2_middle)
    child_2_prefix = fix_pmx(parent_1[:cut_1], child_2_middle, child_1_middle)

    child_1_suffix = fix_pmx(parent_2[cut_2:], child_1_middle, child_2_middle)
    child_2_suffix = fix_pmx(parent_1[cut_2:], child_2_middle, child_1_middle)

    child_1 = child_1_prefix + child_1_middle + child_1_suffix
    child_2 = child_2_prefix + child_2_middle + child_2_suffix

    return child_1, child_2


def crossover(pop, pc):
    new_population = []

    for i in range(0, len(pop), 2):  # idziemy przez osobników co dwa, bo krzyżujemy pary
        parent_1 = pop[i]
        parent_2 = pop[i+1]

        if pc > random.random():
            child_1, child_2 = crossover_pmx(parent_1, parent_2)
        else:
            child_1, child_2 = parent_1, parent_2

        new_population.append(child_1)
        new_population.append(child_2)

    return new_population


# mutation
def inv_mutation(ind):
    m = len(ind)

    cut_1 = random.randint(0, m)
    cut_2 = random.randint(cut_1+1, m+1)
    cut_2 += 1

    mid = ind[cut_1:cut_2]
    ind[cut_1:cut_2] = mid[::-1]


def mutation(pop, pm):
    for ind in pop:
        if pm > random.random():
            inv_mutation(ind)
