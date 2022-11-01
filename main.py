import filecmp
import os
import shutil
import string
import random
from pathlib import Path

from mpps import lib

upload_folder_path = 'X:\\Camera Uploads'
target_folder_template = string.Template('X:\\Photos\\${year}\\${year}-${month}\\${year}-${month}-${day}_PhotosPhone')

if __name__ == '__main__':
    for path in os.scandir(upload_folder_path):
        if path.is_file():
            split_tup = os.path.splitext(path.name)
            match split_tup[1]:
                case '.jpg' | '.JPG' | '.jpeg':
                    print(f"Working on {path.path}")
                    jpeg_date = lib.get_date_from_file(path.path)

                    if jpeg_date is None:
                        print(f"Unable to get date for {path.path}")
                    else:
                        target_folder = lib.get_target_folder(target_folder_template, jpeg_date)
                        target_file = Path(target_folder)/path.name
                        os.makedirs(target_folder, exist_ok=True)
                        if target_file.is_file():
                            if filecmp.cmp(path.path, target_file, shallow=False):
                                print(f"{target_file} already exists and is the same as {path.path}; deleting {path.path}!")
                                os.remove(path.path)
                            else:
                                print(f"{target_file} already exists and is not the same as {path.path}!!!")
                                new_file_name = split_tup[0] + '.' + ''.join(random.choice(string.ascii_letters) for i in range(10)) + split_tup[1]
                                target_file = Path(target_folder) / new_file_name
                                print(f"Moving {path.path} to {target_file}")
                                shutil.move(path.path, target_file)
                        else:
                            print(f"Moving {path.path} to {target_file}")
                            shutil.move(path.path, target_file)

