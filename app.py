from src.csv_utils import *
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

USE = "csv" # csv | sqlite

class MainWindow(QMainWindow):
    def __init__(self, csv: bool):
        super().__init__()
        self.csv = csv
        self.setWindowTitle("Hello")

if __name__ == '__main__':
    csv = USE == "csv"
    if csv:
        header_type: list[type] = [str, float, str, int, str]
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        catalogue = Database()
        catalogue.SAVE_FILE()
    else:
        header_type: list[type] = [str, float, str, int, str]  # Changer pour utiliser du CSV
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])  # Changer pour utiliser du CSV
        catalogue = Database()  # Changer pour utiliser du CSV
        catalogue.SAVE_FILE() # Changer pour utiliser du CSV
        
    app = QApplication(sys.argv)
    window = MainWindow(csv)
    window.show()
    sys.exit(app.exec())