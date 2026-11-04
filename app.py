from assets.utils.csv_utils import Catalogue, Catalogue_Reader, CREATE_CSV
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QPushButton, QListWidget, \
                            QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtCore import QSize, Qt, QRect, QPropertyAnimation
import sys

if __name__ == '__main__':
    header_type: list[type] = [str, str, int]
    CREATE_CSV(header=['test1', 'test2', 'test3'])
    catalogue = Catalogue()
    catalogue.SAVE_CSV()
    reader = Catalogue_Reader(catalogue)
    reader.PRINT_CSV()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle("My App")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()

        button = QPushButton("Press Me !")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        self.setCentralWidget(button)
    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)

app = QApplication(sys.argv)
window = MainWindow()
window.show()


app.exec()