"""
Generate files from template
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, './python')
from simpython.common import template, file_utils  # type: ignore # pylint: disable=import-error,wrong-import-position

if __name__ == '__main__':

    prior = list(range(1, 101))

    # 2nd wave fixed
    cmm = Path('Unisim_iv_2024/dat/sens/2nd_wave_fixed/template.cmm')
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'sch': file_utils.list_files(
            folder_path='Unisim_iv_2024/sch/sens/2024/2nd_wave_fixed',
            with_extensions=False)[::3]
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)


    # 2nd wave wag

    cmm = Path('Unisim_iv_2024/dat/sens/2nd_wave_wag/template.cmm')
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'sch': file_utils.list_files(
            folder_path='Unisim_iv_2024/sch/sens/2024/2nd_wave_wag',
            with_extensions=False)[::3]
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)


    # FPSO max Qg

    cmm = Path('Unisim_iv_2024/dat/sens/plat_max_qg/template.cmm')
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'qgmax': list(range(5, 16))
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)


    # Trigger GOR

    cmm = Path('Unisim_iv_2024/dat/sens/trigger_gor/template.cmm')
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'gormax': [i*100 for i in range(10, 21)]
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)


    # WAG duration

    cmm = Path('Unisim_iv_2024/dat/sens/wag_duration/template.cmm')
    var_dict = {
        'prior': prior,
        'eos': [0],
        'kr': [1],
        'wag_days': [i*20 for i in range(3, 16)][::2]
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)


    # CMOST

    cmm = Path('Unisim_iv_2024/dat/sens/cmost/template.cmm')
    var_dict = {
        'prior': [82, 51, 99, 4, 48], #[82, 35, 51, 76, 99, 72, 4, 22, 48]
        'eos': [0,1,2],
        'kr': [0,1,2],
        'fault': np.logspace(-3, -1, num=3),
        'uw': [0.25,0.35,0.45],
        'woc': np.linspace(5650., 5750., 3),
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)
