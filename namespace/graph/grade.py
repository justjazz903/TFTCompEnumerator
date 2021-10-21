import concurrent.futures
from sys import getsizeof
import pickle

from namespace.graph.grader import simple_grader, poker_grader
from namespace.graph.combination_reducer import reduce_combination_set6
from constant import CONSTANT

def get_scores_size(scores):
    size = 0
    for score in scores.keys():
        size += getsizeof(scores[score])
    return size

def merge_dict(d1, d2):
    for score in d2.keys():
        try:
            d1[score] += d2[score]
        except:
            d1[score] = d2[score]

def poker_grade(trait_number_matrix, base, champion_matrix, trait_matrix, level, reduced_size, max_workers):
    all_comp_id = list()
    reduce_combination_set6([i for i in range(champion_matrix.shape[0])], level, [], reduced_size, all_comp_id)
    scores = dict()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        batch_index = 1
        fs = dict()
        for item in all_comp_id:
            fs[executor.submit(
                poker_grader,
                item[0],
                item[1],
                trait_number_matrix,
                base,
                champion_matrix,
                trait_matrix,
                batch_index,
                len(all_comp_id)
            )] = None
            batch_index += 1
        count = 1
        for f in concurrent.futures.as_completed(fs):
            cur_scores = f.result()
            merge_dict(scores, cur_scores)
            if get_scores_size(scores) >= 64 * 1024 ** 2:
                with open(CONSTANT['PATH']['GRADE'] + f'scores_{count}.pickle', 'wb') as file:
                    pickle.dump(scores, file)
                scores = dict()
                count += 1
            del fs[f]
        if len(scores.keys()) > 0:
            with open(CONSTANT['PATH']['GRADE'] + f'scores_{count}.pickle', 'wb') as file:
                pickle.dump(scores, file)

def simple_grade(trait_level, champion_matrix, trait_matrix, level, reduced_size, max_workers):
    all_comp_id = list()
    reduce_combination_set6([i for i in range(champion_matrix.shape[0])], level, [], reduced_size, all_comp_id)
    scores = dict()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        batch_index = 1
        fs = dict()
        for item in all_comp_id:
            fs[executor.submit(
                simple_grader,
                item[0],
                item[1],
                trait_level,
                champion_matrix,
                trait_matrix,
                batch_index,
                len(all_comp_id)
            )] = None
            batch_index += 1
        count = 1
        for f in concurrent.futures.as_completed(fs):
            cur_scores = f.result()
            merge_dict(scores, cur_scores)
            if get_scores_size(scores) >= 64 * 1024 ** 2:
                with open(CONSTANT['PATH']['GRADE'] + f'scores_{count}.pickle', 'wb') as file:
                    pickle.dump(scores, file)
                scores = dict()
                count += 1
            del fs[f]
        if len(scores.keys()) > 0:
            with open(CONSTANT['PATH']['GRADE'] + f'scores_{count}.pickle', 'wb') as file:
                pickle.dump(scores, file)
