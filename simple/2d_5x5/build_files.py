"""
Generate files from template
"""
import sys
from pathlib import Path

sys.path.insert(0, './python')
from simpython.common import template  # type: ignore # pylint: disable=import-error,wrong-import-position

if __name__ == '__main__':

    cmm = Path('./simple/2d_5x5/train/dat/template.cmm')
    var_dict = {
        'prior': [1, 10, 11, 47, 99],
        'layer': range(0,92),
        'sch': [1,2,3]
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)


    cmm = Path('./simple/2d_5x5/test/dat/template.cmm')
    var_dict = {
        'prior': [27, 14],
        'layer': [0, 1, 2, 3],
        'sch': [1,2,3,4],
        'ip01': [1,2],
        'jp01': [1,2],
        'ii01': [4,5],
        'ji01': [4,5],
    }

    tmpl = template.TemplateProcessor(
        template_path=cmm,
        output_file_path=cmm.parent / 'sens.dat')

    tmpl.build_all_combinations(
        variable_dict=var_dict,
        clear_folder=True,
        zip_file_name='dat_files',
        verbose=True)
