from assets.utils.csv_utils import Database, DB_Reader, CREATE_FILE

if __name__ == '__main__':
    header_type: list[type] = [str, float, str, int, str]
    CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
    catalogue = Database()
    catalogue.SAVE_FILE()
    reader = DB_Reader(catalogue)
    reader.PRINT_TABLE()