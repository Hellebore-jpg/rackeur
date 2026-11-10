from __future__ import annotations
#=============================================================================#
# PARAMETRES DES SCRIPTS HELPERS                                              #
#=============================================================================#
# Ce script stocke les paramètres dont les scripts helpers auront besoin qui ne
# peuvent pas être inclus dans config.py à cause d'une importation "croisée".

CSV: bool | None = None # Type de base de données séléctionné (True => CSV, False => SQLite)