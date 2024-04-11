# Libraries
import random


class Matrix:
    def distance(self, file_name: str):
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


class Population:
    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n

    def new_individual(self) -> list:
        ind = list(range(self.m))
        random.shuffle(ind)
        return ind

    def new_population(self) -> list:
        pop = []
        for _ in range(self.n):
            pop.append(Population.new_individual(self))

        return pop

    def print_ind(self, ind, fit):
        print("-".join(map(str, ind)), fit)

    def print_pop(self, pop, fit=None):
        if not fit:
            fit = ["empty" for _ in range(len(pop))]

        for ind, fits in zip(pop, fit):
            Population.print_ind(ind, fit)


class Fitness:
    def __init__(self, dm):
        self.dm = dm

    def evaluate_individual(self, ind):
        m = len(ind)
        fit = 0
        for i_gene in range(m-1):  # gene m-1
            gene_1 = ind[i_gene]
            gene_2 = ind[i_gene+1]
            fit += self.dm[gene_1][gene_2]

        # from the last to the first gene
        gene_1 = ind[-1]
        gene_2 = ind[0]
        fit += self.dm[gene_1][gene_2]

        return fit

    def evaluate_population(self, pop):
        fit = []

        for ind in pop:
            eval_ind = Fitness.evaluate_individual(self, ind)
            fit.append(eval_ind)

        return fit

    def find_best_individual_index(self, fit):
        # return fitness.index(min(fitness))
        index = 0  # at the beginning index of the frst element but later index of the best element
        for i in range(1, len(fit)):  # all elements verification
            if fit[i] < fit[index]:  # changing for the best (if any)
                index = i
        return index


class Selection:
    def tournament(self, pop, fitness, k):
        n = len(pop)  # number of individuals
        new_pop = []

        for _ in range(n):  # number of tournaments = number of individuals
            best_ind_index = random.randint(0, n-1)

            for _ in range(k-1):
                random_ind_index = random.randint(0, n-1)
                if fitness[random_ind_index] < fitness[best_ind_index]:
                    best_ind_index = random_ind_index

            new_pop.append(pop[best_ind_index][:])

        return new_pop


class Crossover:

    def fix_pmx(self, parent, self_mid, second_mid):
        fix = []

        for gene in parent:
            while gene in self_mid:
                pos = self_mid.index(gene)
                gene = second_mid[pos]

            fix.append(gene)

        return fix

    def crossover_pmx(self, parent_1, parent_2):
        m = len(parent_1)

        cut_1 = random.randint(0, m)
        cut_2 = random.randint(cut_1+1, m+1)
        cut_2 += 1  # for the situation without suffix

        child_1_middle = parent_1[cut_1:cut_2]
        child_2_middle = parent_2[cut_1:cut_2]

        child_1_prefix = Crossover.fix_pmx(self, parent_2[:cut_1], child_1_middle, child_2_middle)
        child_2_prefix = Crossover.fix_pmx(self, parent_1[:cut_1], child_2_middle, child_1_middle)

        child_1_suffix = Crossover.fix_pmx(self, parent_2[cut_2:], child_1_middle, child_2_middle)
        child_2_suffix = Crossover.fix_pmx(self, parent_1[cut_2:], child_2_middle, child_1_middle)

        child_1 = child_1_prefix + child_1_middle + child_1_suffix
        child_2 = child_2_prefix + child_2_middle + child_2_suffix

        return child_1, child_2

    def execute(self, pop, pc):
        new_population = []

        for i in range(0, len(pop), 2):  # crossover for pairs, therefore we select 2
            parent_1 = pop[i]
            parent_2 = pop[i+1]

            if pc > random.random():
                child_1, child_2 = Crossover.crossover_pmx(self, parent_1, parent_2)
            else:
                child_1, child_2 = parent_1, parent_2

            new_population.append(child_1)
            new_population.append(child_2)

        return new_population


class Mutation:
    # inversion
    def inversion(self, ind):
        m = len(ind)

        cut_1 = random.randint(0, m)
        cut_2 = random.randint(cut_1+1, m+1)
        cut_2 += 1

        mid = ind[cut_1:cut_2]
        ind[cut_1:cut_2] = mid[::-1]

    # complex inversion
    def inversion_complex(self, ind):
        m = len(ind)

        cuts = []
        for _ in range(6):
            cuts.append(random.randint(0, m - 1))

        for i in range(0, 5):
            cut_1 = sorted(cuts)[i]
            cut_2 = sorted(cuts)[i + 1]
            mid = ind[cut_1:cut_2 + 1]
            ind[cut_1:cut_2 + 1] = mid[::-1]

    # exchange mutation
    def exchange(self, ind):
        m = len(ind)

        cut_1 = random.randint(0, m - 1)
        cut_2 = random.randint(0, m - 1)

        ind[cut_1], ind[cut_2] = ind[cut_2], ind[cut_1]

    def execute(self, pop, pm, mutation_v):
        for ind in pop:
            if pm > random.random():
                if mutation_v == 'inversion':
                    Mutation.inversion(self, ind)
                elif mutation_v == 'inversion_complex':
                    Mutation.inversion_complex(self, ind)
                elif mutation_v == 'exchange':
                    Mutation.exchange(self, ind)
