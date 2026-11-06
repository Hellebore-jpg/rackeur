from PyQt6.QtCore import QAbstractTableModel, Qt


class ProduitModel(QAbstractTableModel):

    def __init__(self, database):
        super().__init__()

        self.database = database
        self.headers = database.HEAD

        self.produits = database.READER().READ()

    def rowCount(self, parent=None):
        return len(self.produits)

    def columnCount(self, parent=None):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]

        return None

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(
                self.produits[index.row()][index.column()]
            )

        return None

    def actualiser(self):
        self.beginResetModel()

        self.headers = self.database.HEAD
        self.produits = self.database.READER().READ()

        self.endResetModel()
