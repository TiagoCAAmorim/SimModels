"""
Common functions
"""
import sys
import zipfile
from pathlib import Path
import pandas as pd  # pylint: disable=import-error

sys.path.insert(0, './python')


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


def delete_files(folder_path, extensions=None):
    """ Delete all files in a folder with a given extension """
    for f in list_files(folder_path):
        file = folder_path/f
        if (extensions is None) or (file.suffix in extensions):
            file.unlink()


def save_to_csv(header, values, output_file_path):
    """ Save values to a csv file """
    df = pd.DataFrame(values, columns=header)
    df.to_csv(output_file_path, index=True)


def zip_files(folder_path, file_list=None, extensions=None, file_name='archive', delete_original=False):
    """ Zip all files in a folder with a given extension """
    with zipfile.ZipFile(folder_path/f'{file_name}.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
        if file_list is None:
            file_list = list_files(folder_path)
        for filename in file_list:
            if isinstance(filename, str):
                file = folder_path/filename
            else:
                file = filename
            if (extensions is None) or (file.suffix in extensions):
                myzip.write(file, arcname=file.name)
                if delete_original:
                    file.unlink()


if __name__ == '__main__':
    print(__doc__)
