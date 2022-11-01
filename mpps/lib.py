import os
import re
import string
from datetime import date

from PIL import Image
from PIL.ExifTags import TAGS

# '2022:09:25 16:11:28'
re_date_with_full_columns = re.compile(r"\d\d\d\d:\d\d:\d\d")

re_8digits_date = re.compile(r".*(?<!\d)(\d{8})(?!\d).*")
re_date_in_dd_mm_yyyy = re.compile(r".*(?<!\d)(\d{2}-\d{2}-\d{4})(?!\d).*")


def extract_date_from_exif_datetime_tag(tag_value: str) -> date:
    if tag_value is None or not tag_value:
        return None

    match_res = re_date_with_full_columns.match(tag_value)
    if match_res is not None:
        return date.fromisoformat(tag_value[0:10].replace(':', '-'))
    return None


def get_datetime_exif_data_tag_value(jpeg_path: str) -> str:
    image = Image.open(jpeg_path)
    exif_data = image.getexif()
    for tag_id in exif_data:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exif_data.get(tag_id)
        if tag == 'DateTime':
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()

            return data

    return None


def get_date_from_filename(filename: str) -> date:
    match_res = re_8digits_date.match(filename)
    if match_res is not None:
        datestr = match_res.group(1)
        return date(int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:]))

    match_res = re_date_in_dd_mm_yyyy.match(filename)
    if match_res is not None:
        datestr = match_res.group(1)
        return date(int(datestr[6:10]), int(datestr[3:5]), int(datestr[0:2]))

    return None


def get_date_from_file(jpeg_path: str) -> date:
    date_from_exif = extract_date_from_exif_datetime_tag(get_datetime_exif_data_tag_value(jpeg_path))
    if date_from_exif is not None:
        return date_from_exif
    return get_date_from_filename(os.path.basename(jpeg_path))


def get_target_folder(target_folder_template: string.Template, photo_date: date) -> str:
    if photo_date is None or target_folder_template is None:
        return None

    return target_folder_template.substitute(
        year=f'{photo_date.year:04}',
        month=f'{photo_date.month:02}',
        day=f'{photo_date.day:02}'
    )
