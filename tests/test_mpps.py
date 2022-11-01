import datetime
import string
from unittest import TestCase

from mpps import lib


class test_mpps(TestCase):

    def test_extract_date_from_exif_datetime_tag_should_return_date(self):
        res = lib.extract_date_from_exif_datetime_tag('2022:09:25 16:11:28')
        self.assertIsNotNone(res)
        self.assertEqual(res.year, 2022)
        self.assertEqual(res.month, 9)
        self.assertEqual(res.day, 25)

    def test_extract_date_from_exif_datetime_tag_should_return_none(self):
        self.assertIsNone(lib.extract_date_from_exif_datetime_tag(None))
        self.assertIsNone(lib.extract_date_from_exif_datetime_tag(""))
        self.assertIsNone(lib.extract_date_from_exif_datetime_tag('junk 2022:09:25 16:11:28'))

    def test_get_datetime_exif_data_tag_value(self):
        datetime_tag_value = lib.get_datetime_exif_data_tag_value("resources/photo_with_exif_tags.jpg")
        self.assertEqual(datetime_tag_value, "2022:11:01 09:25:27")

    def test_get_date_from_filename(self):
        self.assertEqual(lib.get_date_from_filename("PXL_20221002_092712569.jpg"), datetime.date(2022, 10, 2))
        self.assertEqual(lib.get_date_from_filename("IMG-20221001-WA0007.jpg"), datetime.date(2022, 10, 1))
        self.assertEqual(lib.get_date_from_filename("Seesaw_25-05-2022-11.jpg"), datetime.date(2022, 5, 25))

    def test_get_target_folder(self):
        target_folder_template = string.Template('X:\\Photos\\${year}\\${year}-${month}\\${year}-${month}-${day}_PhotosPhone')
        self.assertEqual(
            lib.get_target_folder(target_folder_template, datetime.date(2022, 2, 1)),
            'X:\\Photos\\2022\\2022-02\\2022-02-01_PhotosPhone'
        )
