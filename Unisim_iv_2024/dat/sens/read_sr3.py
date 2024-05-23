"""
Read all SR3 in a folder and generate CSV files
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd  # pylint: disable=import-error
import shutil
import common

sys.path.insert(0, './python')
from simpython.cmg import sr3reader  # type: ignore # pylint: disable=import-error,wrong-import-position


def make_csv(folder_path):
    """ Builds CSV files """
    days = None
    for file in common.list_files(folder_path):
        if file[-4:] == '.sr3':
            print(f'Reading {file}...')
            sr3 = sr3reader.Sr3Reader(folder_path/file)
            days_ = sr3.get_days('group')
            if days is None:
                days = np.linspace(days_[0], days_[-1], 363)

            if days_[-1] < days[-1]:
                print(f' Incomplete data in {file}.')
                continue

            property_names=['QO','QW','QG','NP','GP','WP','QO_RC','QG_RC','QW_RC']
            element_names=['FIELD-PRO','FIELD-INJ']
            all_data = sr3.get_data(
                 element_type='group',
                 property_names=property_names,
                 element_names=element_names,
                 days=days)
            header = sr3.get_series_order(
                 property_names=property_names,
                 element_names=element_names)
            all_header = [f'{element_}:{property_}' for (element_,property_) in header]
            all_header.insert(0, 'Date')
            df = pd.DataFrame(all_data)
            df.to_csv(folder_path/f"{file[:-4]}_group.csv", header=all_header, index=False)

            property_names=['VOIP','PDTVSEC']
            element_names=['FIELD']
            data = sr3.get_data(
                 element_type='sector',
                 property_names=property_names,
                 element_names=element_names,
                 days=days)
            header = sr3.get_series_order(
                 property_names=property_names,
                 element_names=element_names)
            header_ = [f'{element_}:{property_}' for (element_,property_) in header]
            all_header.extend(header_)
            all_data = np.concatenate((all_data, data[:,1:]), axis=1)

            property_names=['QO','QW','QG','NP','GP','WP','QO_RC','QG_RC','QW_RC','BHP']
            element_names=list(sr3.get_elements('well').keys())
            data = sr3.get_data(
                 element_type='well',
                 property_names=property_names,
                 element_names=element_names,
                 days=days)
            header = sr3.get_series_order(
                 property_names=property_names,
                 element_names=element_names)
            header_ = [f'{element_}:{property_}' for (element_,property_) in header]
            all_header.extend(header_)
            all_data = np.concatenate((all_data, data[:,1:]), axis=1)

            df = pd.DataFrame(all_data)
            df.to_csv(folder_path/f"{file[:-4]}.csv", header=all_header, index=False)


def make_zip(folder_path):
    """ Zips CSV files """
    file_list_group = []
    file_list = []
    for file in common.list_files(folder_path):
        if file[-4:] == '.sr3':
            if (folder_path/f"{file[:-4]}_group.csv").is_file():
                file_list_group.append(folder_path/f"{file[:-4]}_group.csv")
            if (folder_path/f"{file[:-4]}.csv").is_file():
                file_list.append(folder_path/f"{file[:-4]}.csv")
    if len(file_list_group) > 0:
        common.zip_files(
            folder_path=folder_path,
            file_list=file_list_group,
            file_name='group_csv',
            delete_original=True)
    if len(file_list) > 0:
        common.zip_files(
            folder_path=folder_path,
            file_list=file_list,
            file_name='csv',
            delete_original=True)


def move_sr3(folder_path):
    """ Move all sr3 files to a subfolder """
    file_list = []
    for file in common.list_files(folder_path):
        if file[-4:] == '.sr3':
            file_list.append(file)
    if len(file_list) > 0:
        subfolder_path = folder_path / "sr3"
        subfolder_path.mkdir(parents=True, exist_ok=True)
        for filename in file_list:
            source_path = folder_path / filename
            destination_path = subfolder_path / filename
            shutil.move(source_path, destination_path)


def make(folder_path):
    """ Wrapper """
    folder_path=Path(folder_path)
    make_csv(folder_path)
    make_zip(folder_path)
    move_sr3(folder_path)


if __name__ == '__main__':

    folder = 'Unisim_iv_2024/dat/sens/2nd_wave_fixed'
    make(folder)

    folder = 'Unisim_iv_2024/dat/sens/2nd_wave_wag'
    make(folder)

    folder = 'Unisim_iv_2024/dat/sens/plat_max_qg'
    make(folder)

    folder = 'Unisim_iv_2024/dat/sens/trigger_gor'
    make(folder)

    folder = 'Unisim_iv_2024/dat/sens/wag_duration'
    make(folder)
