"""
Read all SR3 in a folder and generate CSV files
"""
import sys
from pathlib import Path
import random
import numpy as np
import pandas as pd  # pylint: disable=import-error
from tqdm import tqdm

sys.path.insert(0, './python')
from simpython.cmg import sr3reader  # type: ignore # pylint: disable=import-error,wrong-import-position
from simpython.common import file_utils  # type: ignore # pylint: disable=import-error,wrong-import-position


def columns():
    """ Columns in the data file """
    return {
        # Static characteristics
        'Por_in':{'element':'grid', 'property':'POR', 'delta_t':None},
        'PermI_in':{'element':'grid', 'property':'PERMI', 'delta_t':None},
        'PermJ_in':{'element':'grid', 'property':'PERMJ', 'delta_t':None},
        # 'PermK_in':{'element':'grid', 'property':'PERMK'},

        # Initial state
        'Pres_in':{'element':'grid', 'property':'PRES', 'delta_t':0},
        'Sw_in':{'element':'grid', 'property':'SW', 'delta_t':0},
        'Kro_in':{'element':'grid', 'property':'KRO', 'delta_t':0},
        'Krw_in':{'element':'grid', 'property':'KRW', 'delta_t':0},

        # Input controls
        'Pwf_in':{'element':'well', 'name':'P01', 'property':'BHP', 'operation':'mean'},
        'QwI_in':{'element':'well', 'name':'I01', 'property':'WP', 'operation':'delta'},

        # Output
        'Pres_out':{'element':'grid', 'property':'PRES', 'delta_t':1},
        'Sw_out':{'element':'grid', 'property':'SW', 'delta_t':1},
        'Kro_out':{'element':'grid', 'property':'KRO', 'delta_t':1},
        'Krw_out':{'element':'grid', 'property':'KRW', 'delta_t':1},

        'Qo_out':{'element':'well', 'name':'P01', 'property':'NP', 'operation':'delta'},
        'Qw_out':{'element':'well', 'name':'P01', 'property':'WP', 'operation':'delta'},
        'PwfI_out':{'element':'well', 'name':'I01', 'property':'BHP', 'operation':'mean'},
    }


def valid_days(sr3):
    """ Check time steps that are exactly one day long """
    days = sr3.get_days('grid')
    days_well = sr3.get_days('well')
    valid = []
    for i, day in enumerate(days[:-1]):
        j = i+1
        while (j<len(days)) and (days[j] - day < 1):
            j += 1
        if days[j] - day > 1.01:
            j = j - 1
            if days[j] - day < 0.99:
                continue
        if day < days_well[0]:
            continue
        if days[j] > days_well[-1]:
            continue
        valid.append(day)
    return valid


def read_data(sr3, days=None):
    """ Reads a SR3 file """

    def _apply_operation(data, operation):
        if operation == 'mean':
            return np.mean(data[:,1])
        if operation == 'delta':
            return data[1,1] - data[0,1]
        if operation == 'max':
            return max(data[1,1], data[0,1])
        if operation == 'min':
            return min(data[1,1], data[0,1])
        if operation == 'first':
            return data[0,1]
        if operation == 'last':
            return data[1,1]
        raise ValueError(f'Invalid operation: {v["operation"]}.')

    sr3.open()
    data = []

    w_inj_final = sr3.get_data(
        element_type='well',
        property_names='WP',
        element_names='I01')[-1]
    np_final = sr3.get_data(
        element_type='well',
        property_names='NP',
        element_names='P01')[-1]
    if w_inj_final[1]*np_final[1] == 0:
        return data

    if days is None:
        days = valid_days(sr3)
    for day in days:
        data_ = {'day':day}
        for k,v in columns().items():
            if v['element'] == 'grid':
                if v['delta_t'] is None:
                    day_ = 0
                else:
                    day_ = day + v['delta_t']
                new_data = sr3.get_grid_data(
                      property_names=v['property'],
                      day=day_,
                      return_complete=True)
            elif v['element'] == 'well':
                new_data = sr3.get_data(
                    element_type='well',
                    property_names=v['property'],
                    element_names=v['name'],
                    days=[day, day+1])
                new_data = _apply_operation(new_data, v['operation'])
            data_[k] = new_data
        data.append(data_)
    sr3.close()
    return data


def _col_type(col_name):
    if col_name[-2:]=='in':
        return 'in'
    if col_name[-3:]=='out':
        return 'out'
    return None


def organize_data(data, wells_ij):
    """ Organizes data into a single line """
    line = {
        'in':None,
        'out':None
    }
    for k,v in columns().items():
        x = _col_type(k)

        if x is not None:
            if isinstance(data[k], np.ndarray):
                if line[x] is None:
                    n_cell = len(data[k])
                    line[x] = data[k].reshape(-1)
                else:
                    line[x] = np.concatenate((line[x], data[k].reshape(-1)), axis=0)
            else:
                array_ = np.zeros(n_cell)
                p = wells_ij[v['name']]
                array_[p] = data[k]
                line[x] = np.concatenate((line[x], array_.reshape(-1)), axis=0)
    return line


def get_wells_positions(file_path, wells, ni, nj):
    """ Returns dict with wells positions """
    df = pd.read_csv(file_path)

    positions = {}
    for index_ in df.index:
        positions[index_] = {}
        for k,v in wells.items():
            ijk = list(v)
            for i, ijk_ in enumerate(ijk):
                if isinstance(ijk_,str):
                    ijk[i] = df[ijk_][index_]
            positions[index_][k] = (ijk[2] - 1)*ni*nj + (ijk[1] - 1)*ni + ijk[0] - 1
    return positions


def build_data_file(folder_path, n_files, ni, nj, nk, output_file_name, wells, var_table_path):
    """ Reads all SR3 files into a single csv """
    folder_path = Path(folder_path)

    names = {'in': [], 'out': []}
    for c in columns():
        k = _col_type(c)
        col = c.replace(f'_{k}','')
        names[k].append(col)
    col_names = {'in': ['index', 'day'], 'out': ['index', 'day']}
    for k,v in names.items():
        for col in v:
            col_names[k].extend(
                [f'{col}_{i}' for i in range(ni*nj*nk)]
            )

    df_in = pd.DataFrame(columns=col_names['in'])
    df_out = pd.DataFrame(columns=col_names['out'])

    wells_ij = get_wells_positions(
        file_path = Path(var_table_path),
        wells=wells,
        ni=ni,
        nj=nj)

    files = file_utils.list_files(folder_path)
    random.seed(42)
    random.shuffle(files)

    for file in tqdm(files[:n_files]):
        if file[-4:] == '.sr3':
            index_ = file.replace('sens_','').replace('.sr3','')
            index_ = int(index_)
            try:
                sr3 = sr3reader.Sr3Reader(folder_path/file)
            except:  # pylint: disable=bare-except
                print(f'Error reading {file}.')
                continue
            data = read_data(sr3)
            if len(data) == 0:
                print(f'Invalid simulation: {file}.')
            else:
                for data_ in data:
                    day = data_['day']
                    lines = organize_data(data_, wells_ij[index_])
                    df_in.loc[len(df_in)] = np.concatenate(([index_], [day], lines['in']))
                    df_out.loc[len(df_out)] = np.concatenate(([index_], [day], lines['out']))

    df_in.to_csv(folder_path/f'X_{output_file_name}', header=df_in.columns, index=True)
    df_out.to_csv(folder_path/f'y_{output_file_name}', header=df_out.columns, index=True)


if __name__ == '__main__':

    options = {
        'folder_path':'./simple/2d_5x5/train/sr3',
        'n_files': 50,
        'var_table_path':'./simple/2d_5x5/train/dat/var_table.csv',
        'ni': 5,
        'nj': 5,
        'nk': 1,
        'output_file_name':'train.csv',
        'wells':{
            'P01':(1,1,1),
            'I01':(5,5,1)
        }
    }

    build_data_file(**options)

    options = {
        'folder_path':'./simple/2d_5x5/test/sr3',
        'n_files': 10,
        'var_table_path':'./simple/2d_5x5/test/dat/var_table.csv',
        'ni': 5,
        'nj': 5,
        'nk': 1,
        'output_file_name':'test.csv',
        'wells':{
            'P01':('ip01','jp01',1),
            'I01':('ii01','ji01',1)
        }
    }

    build_data_file(**options)
