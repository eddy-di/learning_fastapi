import json

from app.celery.helpers.parser import ExcelSheetParser
from app.config.base import FILE_PATH, SHEET_NAME


def test_excel_parser():
    JSON_FILE_PATH = 'app/admin/menu.json'
    parser: list[dict] = ExcelSheetParser(FILE_PATH, SHEET_NAME)
    parsed_data = parser.parse()

    with open(JSON_FILE_PATH, encoding='utf-8') as json_file:
        data = json.load(json_file)
        assert parsed_data == data
