import pickle
import concurrent.futures
from os import listdir
from os.path import isfile, join
import shutil

from namespace.graph.extracter import default_extracter
from constant import CONSTANT

def check_used_champions(used_champions):
    for is_used in used_champions:
        if not is_used:
            return False
    return True

def merge_used_champions(l1, l2):
    if len(l1) != len(l2):
        raise Exception(f'different list length: l1: {len(l1)}, l2: {len(l2)}')
    res = list()
    for i in range(len(l1)):
        res.append(l1[i] or l2[i])
    return res

def get_ordered_score():
    scores = set()
    filenames = [f for f in listdir(CONSTANT['PATH']['GRADE']) if isfile(join(CONSTANT['PATH']['GRADE'], f))]
    for filename in filenames:
        with open(CONSTANT['PATH']['GRADE'] + filename, 'rb') as f:
            data = pickle.load(f)
        for score in data.keys():
            scores.add(score)
    return sorted(list(scores))[::-1]

def extract(level, champion_matrix, trait_matrix, max_workers):
    used_champions = [False for _ in range(champion_matrix.shape[0])]
    extract_cache = list()
    scores = get_ordered_score()
    filenames = [f for f in listdir(CONSTANT['PATH']['GRADE']) if isfile(join(CONSTANT['PATH']['GRADE'], f))]
    for score in scores:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            fs = dict()
            for filename in filenames:
                fs[executor.submit(
                    default_extracter,
                    CONSTANT['PATH']['GRADE'] + filename,
                    score,
                    level,
                    champion_matrix,
                    trait_matrix
                )] = None
            for f in concurrent.futures.as_completed(fs):
                res, cur_used_champions = f.result()
                extract_cache += res
                used_champions = merge_used_champions(used_champions, cur_used_champions)
                del fs[f]
        print(f'score {score} is extracted')
        if check_used_champions(used_champions):
            break
    with open(CONSTANT['PATH']['EXTRACT'] + f'level{level}.pickle', 'wb') as f:
        pickle.dump(extract_cache, f)
    shutil.rmtree(CONSTANT['PATH']['GRADE'])
