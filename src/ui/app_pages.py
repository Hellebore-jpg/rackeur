from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from .gestion_user import GestionUserPage
from .add_product import AddProductPage
from .main_page import MainPage
from .auth_window import AuthWindow
from ..utils import csv_utils, sqlite_utils, utils_config


class AppWindow(QMainWindow):
    """Unique fenêtre de l'application : les pages sont empilées dedans."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rackeur")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self._pages = {
            "main": (MainPage(self)),
            "add_product": (AddProductPage(self)),
            "gestion_user": (GestionUserPage(self)),
            "auth": (AuthWindow(self))
        }

        for page in self._pages.values():
            self.stack.addWidget(page)

    def switch_to(self, title_page: str, index_product: int = -1) -> None:
        page = self._pages.get(title_page)

        if page is None:
            raise ValueError(f"Page inconnue : {title_page}")
        
        if title_page in ("main", "gestion_user", "add_product"):
            if utils_config.CSV:
                page.database = csv_utils.Database("catalogue.csv")
            else:
                page.database = sqlite_utils.Database("catalogue.db")
            if utils_config.CSV:
                page.user_database = csv_utils.Database("utilisateurs.csv")
            else:
                page.user_database = sqlite_utils.Database("utilisateurs.db")

            if title_page == "add_product":
                page.set_product_index(index_product)

            page.refresh()

        self.stack.setCurrentWidget(page)
