import os
import json

from constant import CONSTANT

def init_path():
    with open(CONSTANT['FILE']['JSON'], 'r') as f:
        data = json.load(f)
    path_list = [
        CONSTANT['PATH']['GRADE'],
        CONSTANT['PATH']['EXTRACT'],
        CONSTANT['PATH']['GRAPH']
    ]
    for path in path_list:
        if not os.path.exists(path):
            os.mkdir(path)
