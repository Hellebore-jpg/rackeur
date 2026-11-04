from assets.utils.csv_utils import Catalogue, Catalogue_Reader, CREATE_CSV

if __name__ == '__main__':
    header_type: list[type] = [str, str, int]
    CREATE_CSV(header=['test1', 'test2', 'test3'])
    catalogue = Catalogue()
    catalogue.SAVE_CSV()
    reader = Catalogue_Reader(catalogue)
    reader.PRINT_CSV()