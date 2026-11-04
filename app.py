from assets.utils.csv_utils import Catalogue, Catalogue_Reader, CREATE_CSV

if __name__ == '__main__':
    CREATE_CSV(header=['test1', 'test2', 'test3'], overwrite=True)
    catalogue = Catalogue()
    catalogue.CREATE(['a', 'b', 'c'])
    catalogue.write_csv()