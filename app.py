from src.csv_utils import *

if __name__ == '__main__':
    header_type: list[type] = [str, float, str, int, str]
    CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
    catalogue = Database()
    catalogue.SAVE_FILE()
    catalogue.READER().PRINT_TABLE()