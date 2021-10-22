from math import factorial
from copy import deepcopy
from itertools import combinations

def combination_calculator(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))

# the combination size will be reducted until less or equal to <size>, <include> are the fixed elements added to the preceeding combination
def reduce_combination(population, sample, include, size, result):
    current_size = combination_calculator(len(population), sample)
    if current_size <= size:
        result.append((combinations(population, sample), deepcopy(include)))
        return
    reduce_combination(population[0: -1], sample, include, size, result)
    include.append(population[-1])
    reduce_combination(population[0: -1], sample - 1, include, size, result)
    include.remove(population[-1])

def reduce_combination_set6(population, sample, include, size, result):
    # remove colossus
    colossus = [6, 32, 47]
    for champ_id in colossus:
        population.remove(champ_id)
    for i in range(len(colossus) + 1):
        colossus_comb = combinations(colossus, i)
        for comb in colossus_comb:
            reduce_combination(population, sample - 2 * i, list(comb), size, result)
