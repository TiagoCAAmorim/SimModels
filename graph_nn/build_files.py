"""
Generate files from template
"""
import sys
import itertools
import numpy as np
from pathlib import Path
import common

sys.path.insert(0, './python')
from simpython.common import template  # type: ignore # pylint: disable=import-error,wrong-import-position


def get_all_combinations(dict_of_lists, verbose=False):
    """ Get all combinations """
    all_combinations = list(itertools.product(*dict_of_lists.values()))
    if verbose:
        print(f'Number of combinations: {len(all_combinations)}.')
    return all_combinations


def build_table(variable_dict, output_file_path):
    """ Save all combinations to a CSV file """
    common.save_to_csv(
        header=variable_dict.keys(),
        values=get_all_combinations(variable_dict, verbose=True),
        output_file_path=output_file_path)


def build_files(template_path, var_table_path, output_file_path):
    """ Build all files based on template """
    template.TemplateProcessor(
        template_path=template_path,
        verbose=False,
        variables_table_path=var_table_path,
        output_file_path=output_file_path)


def make(folder_path, variable_dict):
    """ Wrapper """
    print(f'### {folder_path} ###')
    folder_path = Path(folder_path)
    common.delete_files(
        folder_path=folder_path,
        extensions=['.dat','.csv'])
    build_table(
        variable_dict=variable_dict,
        output_file_path=folder_path/'var_table.csv')
    build_files(
        template_path=folder_path/'template.cmm',
        var_table_path=folder_path/'var_table.csv',
        output_file_path=folder_path/'sens.dat')
    common.zip_files(
        folder_path=folder_path,
        extensions=['.dat'],
        file_name='dat_files',
        delete_original=True)


if __name__ == '__main__':

    prior = list(range(1, 101))

    folder = 'graph_nn/2d/dat'
    var_dict = {
        'prior': [1, 10, 11, 47, 99],
        'layer': range(0,92),
        'sch': [1,2,3]
    }
    make(folder_path=folder, variable_dict=var_dict)

    folder = 'graph_nn/2d_test/dat'
    var_dict = {
        'prior': [27, 14],
        'layer': [0, 1, 2, 3],
        'sch': [1,2,3,4],
        'ip01': [1,2],
        'jp01': [1,2],
        'ii01': [4,5],
        'ji01': [4,5],
    }
    make(folder_path=folder, variable_dict=var_dict)
