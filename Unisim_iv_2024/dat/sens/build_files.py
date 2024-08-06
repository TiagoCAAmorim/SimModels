"""
Generate files from template
"""
import sys
import itertools
from pathlib import Path
import numpy as np

sys.path.insert(0, './python')
from simpython.common import template, file_utils  # type: ignore # pylint: disable=import-error,wrong-import-position


def get_all_combinations(dict_of_lists, verbose=False):
    """ Get all combinations """
    all_combinations = list(itertools.product(*dict_of_lists.values()))
    if verbose:
        print(f'Number of combinations: {len(all_combinations)}.')
    return all_combinations


def build_table(variable_dict, output_file_path):
    """ Save all combinations to a CSV file """
    file_utils.save_to_csv(
        values=get_all_combinations(variable_dict, verbose=True),
        output_file_path=output_file_path,
        header=variable_dict.keys())


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
    file_utils.delete_files(
        folder_path=folder_path,
        extensions=['.dat','.csv'])
    build_table(
        variable_dict=variable_dict,
        output_file_path=folder_path/'var_table.csv')
    build_files(
        template_path=folder_path/'template.cmm',
        var_table_path=folder_path/'var_table.csv',
        output_file_path=folder_path/'sens.dat')
    file_utils.zip_files(
        folder_path=folder_path,
        extensions=['.dat'],
        file_name='dat_files',
        delete_original=True)


if __name__ == '__main__':

    prior = list(range(1, 101))

    # 2nd wave fixed

    folder = 'Unisim_iv_2024/dat/sens/2nd_wave_fixed'
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'sch': file_utils.list_files(
            folder_path='Unisim_iv_2024/sch/sens/2024/2nd_wave_fixed',
            with_extensions=False)[::3]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # 2nd wave wag

    folder = 'Unisim_iv_2024/dat/sens/2nd_wave_wag'
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'sch': file_utils.list_files(
            folder_path='Unisim_iv_2024/sch/sens/2024/2nd_wave_wag',
            with_extensions=False)[::3]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # FPSO max Qg

    folder = 'Unisim_iv_2024/dat/sens/plat_max_qg'
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'qgmax': list(range(5, 16))
    }
    make(folder_path=folder, variable_dict=var_dict)


    # Trigger GOR

    folder = 'Unisim_iv_2024/dat/sens/trigger_gor'
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'gormax': [i*100 for i in range(10, 21)]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # WAG duration

    folder = 'Unisim_iv_2024/dat/sens/wag_duration'
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'wag_days': [i*20 for i in range(3, 16)][::2]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # CMOST

    folder = 'Unisim_iv_2024/dat/sens/cmost'
    var_dict = {
        'prior': [82, 51, 99, 4, 48], #[82, 35, 51, 76, 99, 72, 4, 22, 48]
        'eos': [0,1,2],
        'kr': [0,1,2],
        'fault': np.logspace(-3, -1, num=3),
        'uw': [0.25,0.35,0.45],
        'woc': np.linspace(5650., 5750., 3),
    }
    make(folder_path=folder, variable_dict=var_dict)
