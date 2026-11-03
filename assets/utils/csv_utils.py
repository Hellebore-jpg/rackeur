from typing import TypedDict
from pathlib import Path

import csv

class CSVTable(TypedDict):
    header: list[str]
    body: list[list[str]]

class Catalogue:
    def __init__(self, path:str = 'catalogue.csv', delimeter:str = ','):
        self.PATH = Path('assets/data/', path)
        self.DELIMETER = delimeter
        _csv = self.read_csv()
        self.HEAD = _csv['header']
        self.BODY = _csv['body']

    def read_csv(self) -> CSVTable:
        with open(self.PATH, 'r', encoding='utf-8') as f:
            table = list(csv.reader(f, delimiter=self.DELIMETER))
            return {'header': table[0], 'body': table[1:]}

    def write_csv(self):
        with open(self.PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=self.DELIMETER)
            writer.writerow(self.HEAD)
            writer.writerows(self.BODY)

    def csv_format(self, item:object) -> str:
        return str(item)

    def UPDATE(self, item:object|list[object], coords:int|list[int] = 0):
        if isinstance(coords, int) and isinstance(item, list):
            self.BODY[coords] = [self.csv_format(i) for i in item]
        elif isinstance(coords, list):
            self.BODY[coords[0]][coords[1]] = self.csv_format(item)
        else:
            print('Error : Cannot add a single item to replace an entire line.')