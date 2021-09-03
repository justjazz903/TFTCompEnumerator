import pickle
import networkx as nx
from os import listdir
from os.path import isfile, join

from namespace.graph.connector import connector
from constant import CONSTANT

def load_extract():
    filenames = sorted([f for f in listdir(CONSTANT['PATH']['EXTRACT']) if isfile(join(CONSTANT['PATH']['EXTRACT'], f))])
    res = list()
    for filename in filenames:
        with open(CONSTANT['PATH']['EXTRACT'] + filename, 'rb') as f:
            res.append(pickle.load(f))
    return res

def connect(max_diff, champ_num):
    G = nx.DiGraph()
    extract = load_extract()
    bad = set()
    good = dict()
    for i, bit_code in enumerate(extract[0]):
        connector(bit_code, extract, 0, [], good, bad, G, max_diff, champ_num)
        print(f'{i + 1} / {len(extract[0])} is connected')
    with open(CONSTANT['PATH']['GRAPH'] + 'graph.pickle', 'wb') as f:
        pickle.dump(G, f)
    nx.write_graphml(G, CONSTANT['PATH']['GRAPH'] + 'graph.graphml')
