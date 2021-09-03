import numpy as np
from copy import deepcopy
from networkx.utils import pairwise

from namespace.graph.coder import bit_code_to_comp_vec

def is_similar(bc1, bc2, max_diff, champ_num):
    vec1 = bit_code_to_comp_vec(bc1, champ_num)
    vec2 = bit_code_to_comp_vec(bc2, champ_num)
    sum1 = np.sum(vec1)
    sum2 = np.sum(vec2)
    if sum1 > sum2:
        raise Exception('vec1 is longger than vec2')
    sum3 = np.sum(vec1 * vec2)
    return (sum1 - sum3) + (sum2 - sum1) <= max_diff

def get_similars(target_bit_code, bit_code_list, max_diff, champ_num):
    res = list()
    for cur_bit_code in bit_code_list:
        if is_similar(target_bit_code, cur_bit_code, max_diff, champ_num):
            res.append(cur_bit_code)
    return res

def connector(bit_code, extract, index, visited, good, bad, graph, max_diff, champ_num):
    if index == len(extract) - 1:
        visited.append(bit_code)
        for i, bit_code in enumerate(visited):
            graph.add_node(bit_code, layer=i)
        for u, v in pairwise(visited):
            graph.add_edge(u, v)
        visited = visited[:-1]
        return
    if bit_code in bad:
        return
    if bit_code in good.keys():
        similars = good[bit_code]
    else:
        similars = get_similars(bit_code, extract[index + 1], max_diff[index], champ_num)
    if len(similars) > 0:
        good[bit_code] = similars
        for similar in similars:
            visited.append(bit_code)
            connector(similar, extract, index + 1, deepcopy(visited), good, bad, graph, max_diff, champ_num)
            visited = visited[:-1]
    else:
        bad.add(bit_code)
