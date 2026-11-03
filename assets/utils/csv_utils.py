from typing import TypedDict
from pathlib import Path
import csv

class CSVTable(TypedDict):
    header: list[str]
    body: list[list[str]]

def CREATE_BLANK_CSV(path:str|Path, head:list[str], delimeter:str = ',') -> tuple[str|Path, str]:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=delimeter)
        writer.writerow(head)
    return path, delimeter

def list_to_str(item:list[object], padding:int = 0) -> str:
    items = [str(i) for i in item]
    return ' | '.join([e + (padding-len(e))*' ' for e in items])

def PRINT_CSV(head:list[object], body:list[object]|list[list[object]], pretty:bool = True):
    padding = 0
    if pretty:
        for e in head:
            padding = max(padding, len(str(e)))
        for e in body:
            if isinstance(e, list):
                for i in e:
                    padding = max(padding, len(str(i)))
            else: padding = max(padding, len(str(e)))
    print(list_to_str(head, padding))
    if isinstance(body[0], list):
        for e in body:
            print(list_to_str(e, padding))
    else:
        print(list_to_str(body, padding))

def to_type(item:object, rtype:type|None) -> object:
    if rtype is None:
        return item
    return rtype(item)

def csv_format(item:object) -> str:
    return str(item) # Modif pour s'adapter au format des entrées csv pour éviter les problèmes d'indentation
    # Escape delimeter

class Catalogue:
    def __init__(self, path:str|Path = 'catalogue.csv', delimeter:str = ','):
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

    def CREATE(self, item:list[object], index:int = -1):
        insert = [csv_format(i) for i in item]
        if index < 0:
            self.BODY.append(insert)
        self.BODY.insert(index, insert)

    def READ(self, coords:int|list[int] = 0, rtype:type|None = None) -> list[object]|object:
        # Pour lire le corps complet il suffit d'appeller Catalogue.BODY
        if isinstance(coords, int):
            return [to_type(i, rtype) for i in self.BODY[coords]]
        else:
            return to_type(self.BODY[coords[0]][coords[1]], rtype)

    def UPDATE(self, item:object|list[object], coords:int|list[int] = 0):
        if isinstance(coords, int) and isinstance(item, list):
            self.BODY[coords] = [csv_format(i) for i in item]
        elif isinstance(coords, list) and not isinstance(item, list):
            self.BODY[coords[0]][coords[1]] = csv_format(item)
        else:
            print('Error : Cannot add a single item to replace an entire line.')

    def DELETE(self, index:int = -1) -> object:
        return self.BODY.pop(index)