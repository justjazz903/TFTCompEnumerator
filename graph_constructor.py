import os

from namespace.graph.json_processor import get_data_matrix
from namespace.graph.grade import poker_grade, simple_grade
from namespace.graph.extract import extract
from namespace.graph.connect import connect
from namespace.util.path_initializer import init_path

if __name__ == '__main__':
    levels = [5, 6, 7, 8, 9]
    max_diff = [2, 2, 2, 2]
    trait_level = 2
    # base = 1.5
    max_workers = None
    reduced_size = 3162510 # C(54, 5) = 3162510

    champion_matrix, trait_matrix, trait_number_matrix = get_data_matrix()

    for level in levels:
        init_path()
        # poker_grade(trait_number_matrix, base, champion_matrix, trait_matrix, level, reduced_size, max_workers)
        simple_grade(trait_level, champion_matrix, trait_matrix, level, reduced_size, max_workers)
        extract(level, champion_matrix, trait_matrix, max_workers)
    connect(max_diff, champion_matrix.shape[0])
