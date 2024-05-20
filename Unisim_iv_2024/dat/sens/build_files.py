"""
Generate files from template
"""
import sys
import itertools
import zipfile
from pathlib import Path
import pandas as pd  # pylint: disable=import-error

sys.path.insert(0, './python')
from simpython.common import template  # type: ignore # pylint: disable=import-error,wrong-import-position


def list_files(folder_path, with_extensions=True):
    """ List files names in folder """
    try:
        folder_path = Path(folder_path)
        if with_extensions:
            filenames = [file.name for file in folder_path.iterdir() if file.is_file()]
        else:
            filenames = [file.stem for file in folder_path.iterdir() if file.is_file()]
        filenames.sort()
        return filenames
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
        return []


def get_all_combinations(dict_of_lists):
    """ Get all combinations """
    all_combinations = list(itertools.product(*dict_of_lists.values()))
    return all_combinations


def save_to_csv(header, values, output_file_path):
    """ Save values to a csv file """
    df = pd.DataFrame(values, columns=header)
    df.to_csv(output_file_path, index=True)


def build_table(variable_dict, output_file_path):
    """ Save all combinations to a CSV file """
    save_to_csv(header=variable_dict.keys(),
                values=get_all_combinations(variable_dict),
                output_file_path=output_file_path)


def build_files(template_path, var_table_path, output_file_path):
    """ Build all files based on template """
    template.TemplateProcessor(
        template_path=template_path,
        verbose=False,
        variables_table_path=var_table_path,
        output_file_path=output_file_path)

def zip_files(folder_path):
    with zipfile.ZipFile(folder_path/'dat_files.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
        for filename in list_files(folder_path):
            if filename[-4:] in ['.dat','.csv'] :
                myzip.write(folder_path/filename, arcname=filename)

def make(folder_path, variable_dict):
    """ Wrapper """
    folder_path = Path(folder_path)
    build_table(
        variable_dict=variable_dict,
        output_file_path=folder_path/'var_table.csv')
    build_files(
        template_path=folder_path/'template.dat',
        var_table_path=folder_path/'var_table.csv',
        output_file_path=folder_path/'sens.dat')
    zip_files(folder_path)


if __name__ == '__main__':

    # 2nd wave fixed

    folder = 'Unisim_iv_2024/dat/sens/2nd_wave_fixed'
    var_dict = {
        'prior': list(range(1, 5)),
        'eos': [0],
        'kr': [1],
        'sch': list_files('Unisim_iv_2024/sch/sens/2024/2nd_wave_fixed', with_extensions=False)[::5]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # 2nd wave wag

    folder = 'Unisim_iv_2024/dat/sens/2nd_wave_wag'
    var_dict = {
        'prior': list(range(1, 5)),
        'eos': [0],
        'kr': [1],
        'sch': list_files('Unisim_iv_2024/sch/sens/2024/2nd_wave_wag', with_extensions=False)[::5]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # FPSO max Qg

    folder = 'Unisim_iv_2024/dat/sens/plat_max_qg'
    var_dict = {
        'prior': list(range(1, 5)),
        'eos': [0],
        'kr': [1],
        'qgmax': list(range(5, 16))
    }
    make(folder_path=folder, variable_dict=var_dict)


    # Trigger GOR

    folder = 'Unisim_iv_2024/dat/sens/trigger_gor'
    var_dict = {
        'prior': list(range(1, 5)),
        'eos': [0],
        'kr': [1],
        'gormax': [i*100 for i in range(10, 21)]
    }
    make(folder_path=folder, variable_dict=var_dict)


    # WAG duration

    folder = 'Unisim_iv_2024/dat/sens/wag_duration'
    var_dict = {
        'prior': list(range(1, 5)),
        'eos': [0],
        'kr': [1],
        'wag_days': [i*20 for i in range(3, 16)]
    }
    make(folder_path=folder, variable_dict=var_dict)
