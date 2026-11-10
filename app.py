from __future__ import annotations

from PyQt6.QtGui import (
    QIcon,
)
from PyQt6.QtWidgets import (
    QApplication, QDialog,
)

import sys

from src.utils.bootstrap import load_database
from src.utils.helpers import load_stylesheet
from src import config
from src.utils import utils_config

#=============================================================================#
# IMPORTATION DES FENÊTRES                                                    #
#=============================================================================#
from src.ui.source_dialog import SourceDialog
from src.ui.auth_window import AuthWindow
from src.ui.splash import SplashDialog

#=============================================================================#
# DEMARRAGE DE L'APPLICATION                                                  #
#=============================================================================#
def main() -> int:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(config.FAVICON_PATH)))
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
 
    # Demande le type de BDD à l'utilisateur
    dialog = SourceDialog()
    if dialog.exec() != QDialog.DialogCode.Accepted.value:
        return 0  # Quitter l'app si l'utilisateur ferme la fenêtre sans choisir
 
    # Charger la base de données
    utils_config.CSV = dialog.is_csv()
    load_database()
    
    SplashDialog().exec()
 
    # Afficher la fenêtre de connexion
    window = AuthWindow()
    window.showMaximized()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())