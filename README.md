# Rackeur
Développement d'une application de gestion d'un catalogue de materiel de concerts et d'événements. Les visiteurs peuvent consulter le catalogue et acheter des produits. Un panel administrateur complet permet aux gestionnaires et éditeurs de gérer les données des produits.

<img src="md_files\latest_app_screenshot.png" alt="Dernière capture d'écran de l'application" width="800">

## Sommaire
- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Setup](#setup)
    - [Prerequis](#prerequis)
    - [Compatibilité](#compatibilité)
    - [Installation](#installation)
    - [Administration & Edition](#administration--edition)
- [Arborescence](#arborescence)
- [Autheur](#autheur)
- [Crédits](#crédits)
    - [APIs et Dépendences](#apis-et-dépendences)

## Fonctionnalités

- Un catalogue qui affiche les produits disponibles et leurs informations
- Navigation des produits par catégories et recherche
- Achât des produits
- Panel administrateur complet (gère les produits, permissions, etc...)
- PoLP "Principle of Least Privilege" ou Principe du Moindre Privilège
- Alertes automatique en cas de fuite du mot de passe de l'utilisateur

## Technologies

- Python 3.15.0
- CSV puis SQLite

## Setup

### Prerequis

- [Python](https://www.python.org/downloads/) installé

### Compatibilité

Testé avec :

| Logiciel  | Version / détails |
|-----------|-------------------|
| OS        | Windows 11 26h2   |
| Python    | 3.15.0            |

### Installation

1. Cloner le dépot dans le dossier de votre choix :
    ```bash
    cd chemin/vers/votre/dossier
    git clone https://github.com/Hellebore-jpg/rackeur.git rackeur
    ```
2. Ouvrir le dossier dans un terminal et entrer les commandes `python -m venv .venv` pour créer un environement virtuel.
3. Activez l'environement venv avec `.venv\Scripts\Activate.ps1`, puis importez les dépendances avec `pip install -r requirements.txt`.
4. Exécutez le script [app.py](app.py). (`python app.py`)

### Administration & Edition

Disponible pour les utilisateurs aillant des permissions d'administrateur ou d'éditeur.
Le panel ne montre que les outils dont l'administrateur/éditeur à acces selon ses permissions.

| Nom d'utilisateur | Mot de passe |
|-------------------|--------------|
| `admin`           | `123456789`  |
| `editor`          | `123456789`  |

> Ces identifiants ne servent qu'à faire des test, veuillez les changer dès que possible.

## Arborescence

```
rackeur/
├── assets/ → Stockage des ressources
│   ├── data/   → Ressources & Base de données
│   │   ├── catalogue.csv       → Base de données du catalogue de produits format CSV
│   │   └── utilisateurs.csv    → Base de données des utilisateurs format CSV
│   ├── font/   → Polices d'écriture
│   ├── img/    → Images
│   └── style.qss   → Feuille de style PyQt
├── src/    → Scripts Python
│   ├── pages/  → Scripts de fenêtres PyQt
│   ├── utils/  → Scripts utilitaires
│   └── config.py   → Configuration globale
├── app.py  → Application
└── requirements.txt    → Dépendences de l'environement
```

## Autheur

Fait par **4 collaborateurs** pour le projet **Développement Sécurisé** à Guardia CS, 2026 :

- [Hellebore-jpg / Mathieu](https://github.com/Hellebore-jpg) Chef de projet
- [chummel-ops / Charles](https://github.com/chummel-ops)
- [ylavallee-prog / Yanis](https://github.com/ylavallee-prog)
- [Purple-key-0 / Gabriel](https://github.com/Purple-key-0)

## Credits

### APIs et Dépendences
- [PyQt6](https://pypi.org/project/PyQt6/)
- [Requests](https://pypi.org/project/requests/)
- [Bcrypt](https://pypi.org/project/bcrypt/)
- [API Have I Been Pwned](https://www.openstreetmap.org/)