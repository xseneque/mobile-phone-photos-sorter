import filecmp
import os
import shutil
import string
import random
import argparse
from pathlib import Path

from mpps import lib

# --source Z:\Photos\Uploads --target Z:\Photos\Jpeg
target_folder_template = string.Template('${year}/${year}-${month}/${year}-${month}-${day}_PhotosPhone')


def main(args):
    check_dir_exists_or_die(args.target)
    check_dir_exists_or_die(args.source)

    for path in os.scandir(args.source):
        if path.is_file():
            split_tup = os.path.splitext(path.name)
            match split_tup[1]:
                case '.jpg' | '.JPG' | '.jpeg':
                    process_jpg(path, split_tup, args.target)


def check_dir_exists_or_die(directory):
    if directory is None or not os.path.isdir(directory):
        print(f"directory {directory} doesn't exist!")
        exit(1)


def process_jpg(path, split_tup, target_folder):
    src_path = path.path
    print(f"Working on {src_path}")
    jpeg_date = lib.get_date_from_file(src_path)
    if jpeg_date is None:
        print(f"Unable to get date for {src_path}")
    else:
        target_folder = lib.get_target_folder(target_folder, target_folder_template, jpeg_date)
        target_file = Path(target_folder) / path.name
        os.makedirs(target_folder, exist_ok=True)
        if target_file.is_file():
            if filecmp.cmp(src_path, target_file, shallow=False):
                delete_duplicate(src_path, target_file)
            else:
                move_and_rename_file(split_tup, src_path, target_file, target_folder)
        else:
            move_file(src_path, target_file)


def move_and_rename_file(split_tup, src_path, target_file, target_folder):
    print(f"{target_file} already exists and is not the same as {src_path}!!!")
    new_file_name = split_tup[0] + '.' + ''.join(
        random.choice(string.ascii_letters) for i in range(10)) + split_tup[1]
    target_file = Path(target_folder) / new_file_name
    move_file(src_path, target_file)


def delete_duplicate(src_path, target_file):
    print(
        f"{target_file} already exists and is the same as {src_path}; deleting {src_path}!")
    os.remove(src_path)


def move_file(src_path, target_file):
    print(f"Moving {src_path} to {target_file}")
    shutil.move(src_path, target_file)


def get_cmdline_args():
    parser = argparse.ArgumentParser(
        prog='chronological-photo-sorter',
        description='This tool goes through the image files (jpg supported only at this time) in a folder and moves '
                    'them in a hierarchical folder structure. Picture metadata or filenames are used.')
    parser.add_argument('-s', '--source')
    parser.add_argument('-t', '--target')
    return parser.parse_args()

if __name__ == '__main__':
    main(get_cmdline_args())

