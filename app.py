from assets.utils.csv_utils import Catalogue, Catalogue_Reader, CREATE_FILE

if __name__ == '__main__':
    header_type: list[type] = [str, str, int]
    CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
    catalogue = Catalogue()
    catalogue.SAVE_FILE()
    reader = Catalogue_Reader(catalogue)
    reader.PRINT_TABLE()