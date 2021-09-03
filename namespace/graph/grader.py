import numpy as np

from namespace.graph.comp_processor import get_comp_matrix
from namespace.graph.coder import comp_id_to_bit_code

def simple_strategy(trait, trait_level):
    if (trait >= trait_level).any():
        return np.sum(trait)
    else:
        return 0

def poker_strategy(trait, trait_matrix, trait_number_matrix, base):
    count = [0 for _ in range(int(np.max(trait_number_matrix)))]
    active_number = trait_number_matrix[np.where(trait != 0), trait[np.where(trait != 0)]].reshape(-1)
    for number in active_number:
        count[int(number) - 1] += 1
    score = 0
    for i, c in enumerate(count):
        score += c * (base ** i)
    return score


def simple_grader(combination_generator, include, trait_level, champion_matrix, trait_matrix, batch_index, total_batch):
    scores = dict()
    for c in combination_generator:
        comp_id = list(c) + include
        trait, _ = get_comp_matrix(comp_id, champion_matrix, trait_matrix)
        bit_code = comp_id_to_bit_code(comp_id)
        score = simple_strategy(trait, trait_level)
        try:
            scores[score].append(bit_code)
        except:
            scores[score] = [bit_code]
    print(f'batch {batch_index} / {total_batch} graded')
    return scores

def poker_grader(combination_generator, include, trait_number_matrix, base, champion_matrix, trait_matrix, batch_index, total_batch):
    scores = dict()
    for c in combination_generator:
        comp_id = list(c) + include
        trait, _ = get_comp_matrix(comp_id, champion_matrix, trait_matrix)
        bit_code = comp_id_to_bit_code(comp_id)
        score = poker_strategy(trait, trait_matrix, trait_number_matrix, base)
        try:
            scores[score].append(bit_code)
        except:
            scores[score] = [bit_code]
    print(f'batch {batch_index} / {total_batch} graded')
    return scores
