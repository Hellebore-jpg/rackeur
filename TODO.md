# Backlog

## Sommaire
- [Kick off](#kick-off)
- [v1.0](#v10)
    - [Esthétique](#esthétique)
    - [Définisions & Recherches](#définisions--recherches)
    - [Programmation Backend](#programmation-backend)
    - [Programmation Frontend](#programmation-frontend)
    - [Jeux & Bases de données](#jeux--bases-de-données)
    - [Organisation & Finalisation](#organisation--finalisation)
- [v2.0](#v20)

# Kick off
>03/11/2026

## Organisation
- [x] Rôles dans le groupe - **Tout le monde**
    > `Hellebore-jpg` : Chef de projet
    > `chummel-ops` : Responsable de communication
- [x] Répartition du travail

## Configuration
- [x] Git & venv - **Hellebore-jpg**
    >- Création du repo Github et de la base
    >- Ajout des collaborateurs : `Hellebore-jpg (Mathieu)` | `Purple-key-0 (Gabriel)` | `chummel-ops (Charles)` | `ylavallee-prog (Yanis)`
    >- Ajout de l'intervenant : `TheLegacy33`
    >- Explications du fonctionnement de venv à tout le monde et setup sur tout les PCs
    >- Création du [.gitignore](.gitignore) et de [requirements.txt](requirement.txt) avec `pip freeze > requirements.txt`

# V1.0
>03/11/2026 - 13/11/2026

## Objectifs

### Esthétique
- [x] Création d'une Diréction Artistique + Logo + Nom d'app - **chummel-ops**
- [x] Maquette finale des pages de l'aplication
    <img src="md_files\title.png" alt="Titre" width="300"> <img src="md_files\login.png" alt="Connexion" width="300"> <img src="md_files\catalog.png" alt="Catalogue" width="300"> <img src="md_files\admin.png" alt="Panel Admin" width="300"> <img src="md_files\search.png" alt="Recherche" width="300"> <img src="md_files\add_product.png" alt="Ajout de produit" width="300"> <img src="md_files\del_product.png" alt="Supression de produit" width="300">
    
    - [x] Titre - **chummel-ops**
    - [x] Création d'un compte utilisateur et autentification - **chummel-ops**
    - [x] Gestion de produits
        - [x] Affichage de la liste des produits, avec critères de tri - **chummel-ops**
        - [x] Affichage et modification de la liste des produits, pour les admins - **chummel-ops**
        - [x] Recherche d'un produit en fonction d'un ou plusieurs mots-clés - **chummel-ops**
        - [x] Ajout d'un produit - **chummel-ops**
        - [x] Suppression d'un produit - **chummel-ops**

### Définisions & Recherches
- [x] Définition de l'entité "utilisateur" avec prise en compte des différents rôles - **Hellebore-jpg**
    >- Visiteur : Consultation Publique
    >- Utilisateur : Compte & Achâts
    >- Administrateur : Gestion des données du catalogue
- [x] Définition des sigles HMI, GUI, UI et UX - **Hellebore-jpg**
    >- HMI (Human-Machine Interface) : Interface homme-machine, souvent industrielle, pour le contrôle de systèmes.
    >- GUI (Graphical User Interface) : Interface utilisateur graphique, axée sur les éléments visuels et graphiques.
    >- UI (User Interface) : Interface utilisateur, désignant les éléments visuels et interactifs d'un logiciel.
    >- UX (User Experience) : Expérience utilisateur, centrée sur la satisfaction et le parcours global de l'utilisateur.
- [x] Recherches, analyses, et synthèse autour du SGBD SQLite pour le passage CSV a SQLite - **ylavallee-prog** - **Hellebore-jpg**
- [x] Recherches, analyses, et synthèse autour des solutions disponibles pour l'interface utilisateur en Python - **Purple-key-0** - **Hellebore-jpg**
    | Module  | Avantages                                                | Inconvénients                                                                               |
    |---------|----------------------------------------------------------|---------------------------------------------------------------------------------------------|
    | PyQt6   | Puissant, grande flexibilité, widgets riches.            | Courbe d'apprentissage plus raide et des contraintes de licence (Open source obligatoire).  |
    | Tkinter | Standard, intégré à Python, facile à apprendre et léger. | Apparence datée, documentation parfois insuffisante, limites face aux interfaces complexes. |
- [x] Choix d'une solution pour l'interface utilisateur de l'application de gestion du catalogue de produits. - **chummel-ops**

### Programmation Backend
>Implémentation de toutes les fonctionnalitées de l'application à assigner aux boutons de l'interface.
- [x] Script Python d'interaction CSV CRUD
    - [x] 1ère affichage, en ligne de commande, de la liste des produits ( R ) - **Hellebore-jpg**
    - [x] 1ère affichage, en ligne de commande, via une option, de la liste des produits, triés par nom, dans l'ordre alphabétique, et alphabétique inverse ( R ) - **Hellebore-jpg**
    - [x] 1ère affichage, en ligne de commande, via une option, de la liste des produits, triés par prix, dans l'ordre croissant, et décroissant ( R ) - **Hellebore-jpg**
    - [x] 1ère affichage, en ligne de commande, via une option, du ou des produits, en fonction d'un mot-clé (recherche d'un produit dans le catalogue) ( R ) - **Hellebore-jpg**
    - [x] Recherche par catégories - **Hellebore-jpg**
    - [x] Ajout, modification, et suppression d'un produit, en ligne de commande, via une ou plusieurs options ( C U D ) - **Hellebore-jpg**
- [x] Scripts Python de gestion utilisateurs
    - [x] Implémentation du mécanisme d'authentification (Connexion & Inscription) - **Hellebore-jpg**
    - [x] Hash des mots de passe en Bcrypt dans la base de données - **Hellebore-jpg**
    - [x] Gestion des autorisations, sur les 4 opérations sur le catalogue de produits, en ligne de commande, via une ou plusieurs options - **Hellebore-jpg**
    - [x] Implémentation de la création d'un nouvel utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer, au moyen de l'API RESTful "Have I Been Pwned", en ligne de commande, via une ou plusieurs options - **Hellebore-jpg**
    - [x] Implémentation d'un système de notification en cas de nouveaux compromis détectés pour un utilisateur - **Hellebore-jpg** 
- [x] Passage du CSV à SQLite
    - [x] Choix du type de base de données au démarrage & branches différentes pour le SQLite dans les scripts qui utilisent la BDD - **Hellebore-jpg**
        >Exemple :
        >```python
        >if format_bdd == True:
        >   {code_spécifique_à_la_BDD_format_CSV}
        >else:
        >   {code_spécifique_à_la_BDD_format_SQLite}
        >```
    - [x] Écriture du script d'interaction avec la BDD SQLite
        - [x] Affichage de la liste des produits ( R ) - **ylavallee-prog** - **Hellebore-jpg**
        - [x] Affichage, via une option, de la liste des produits, triés par nom, dans l'ordre alphabétique, et alphabétique inverse ( R ) - **ylavallee-prog** - **Hellebore-jpg**
        - [x] Affichage, via une option, de la liste des produits, triés par prix, dans l'ordre croissant, et décroissant ( R ) - **ylavallee-prog** - **Hellebore-jpg**
        - [x] Affichage, via une option, du ou des produits, en fonction d'un mot-clé (recherche d'un produit dans le catalogue) ( R ) - **ylavallee-prog** - **Hellebore-jpg**
        - [x] Recherche par catégories - **ylavallee-prog** - **Hellebore-jpg**
        - [x] Ajout, modification, et suppression d'un produit, via une ou plusieurs options ( C U D ) - **ylavallee-prog** - **Hellebore-jpg**

### Programmation Frontend
>Implémentation des différents composants de l'interface utilisateur.
- [x] Création d'un compte utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer - **Purple-key-0** - **Hellebore-jpg**
- [x] Authentification - **Purple-key-0** - **Hellebore-jpg**
- [x] Gestion de produits
    - [x] Affichage de la liste des produits - **Purple-key-0** 
    - [x] Recherche d'un produit en fonction d'un ou plusieurs mots-clés - **Purple-key-0** 
    - [x] Ajout d'un produit - **Purple-key-0** 
    - [x] Modification d'un produit - **Purple-key-0** 
    - [x] Suppression d'un produit - **Purple-key-0**  
- [x] Panel de gestion des utilisateurs admins et de leur permissions - **Purple-key-0**

### Jeux & Bases de données
- [x] Création du Catalogue / Tableau de données - **Purple-key-0**
    | product        | price  | description                                                                               | stock | quality  |
    |----------------|--------|-------------------------------------------------------------------------------------------|-------|----------|
    | Guitare Fender | 100.00 | Guitare électrique Fender Stratocaster, modèle classique avec un son riche et polyvalent. | 15    | Neuf     |
    | Batterie Pearl | 500.00 | Batterie acoustique Pearl, modèle classique avec un son riche et polyvalent.              | 15    | Bon état |
    | Basse Ibanez   | 500.00 | Basse électrique Ibanez, modèle classique avec un son riche et polyvalent.                | 15    | Correcte |
    | Contre-Basse   | 500.00 | Contre-basse acoustique, modèle classique avec un son riche et polyvalent.                | 15    | Bon état |
- [x] Création manuelle d'un jeu d'essais (Données de tests) dans la table "utilisateur". - **Hellebore-jpg**
    | username      | password                                                        | role    |permissions |
    |---------------|-----------------------------------------------------------------|---------|------------|
    | admin         | \$2b\$12\$ruxeVHj1j5e3UPwHvbCMyufY/qinDTxo2liFTlvcr7nXEva.qqhKe | admin   |1111        |
    | editor        | \$2b\$12\$ruxeVHj1j5e3UPwHvbCMyufY/qinDTxo2liFTlvcr7nXEva.qqhKe | editor  |0110        |
    | remitatouille | \$2b\$12\$ruxeVHj1j5e3UPwHvbCMyufY/qinDTxo2liFTlvcr7nXEva.qqhKe | visitor |0100        |

    >\$2b\$12\$ruxeVHj1j5e3UPwHvbCMyufY/qinDTxo2liFTlvcr7nXEva.qqhKe = 123456789
- [x] Création manuelle du catalogue de produits sous la forme d'une table SQLite (Première BDD SQLite) - **ylavallee-prog** - **Hellebore-jpg**
    >Idem que les jeux de données visibles au dessus.
- [x] Jeu de données de test CSV/SQLite à installer optionellement pendant le setup de l'application - **chummel-ops**

### Organisation & Finalisation
- [x] Relécture et analyse du Cahier des Charges - **chummel-ops** - **Purple-key-0**
- [x] Creation, organisation, écriture et mise à jour du [TODO](TODO.md) (backlogs) - **chummel-ops** - **Hellebore-jpg**
- [x] Explication du code Python (commentaires & Types strictes) - **Hellebore-jpg**
- [x] Rédaction du [README](README.md) - **Hellebore-jpg**
- [x] Canva de présentation de fin de projet - **chummel-ops**
- [x] Ajout des bases de données (CSV & SQLite) dans le [.gitignore](.gitignore) - **chummel-ops**
- [x] Création de l'executable compilé en machine code avec nuitka (Windows) - **Hellebore-jpg**
    >python -m nuitka --standalone --onefile --enable-plugin=pyqt6 --windows-disable-console --windows-icon-from-ico=./assets/img/favicon.ico --include-data-dir=assets=./assets app.py
- [ ] Création de l'executable compilé en machine code avec nuitka (Linux) - **Hellebore-jpg**
    >python -m nuitka --standalone --onefile --enable-plugin=pyqt6 --windows-disable-console --windows-icon-from-ico=./assets/img/favicon.ico --include-data-dir=assets=./assets app.py
- [x] Derniers fix & Publication - **Hellebore-jpg**
- [ ] Release Github

# V2.0
>13/11/2026 +

## Objectifs
- [ ] Navigation par catégories dans l'interface - **Purple-key-0**
- [ ] Profil utilisateur pour changer ses informations - **Hellebore-jpg**
- [ ] Système de commandes des produits - **Hellebore-jpg**
- [ ] Historique des commandes - **Hellebore-jpg**
- [ ] Base de données MySQL en ligne - **Hellebore-jpg**
- [ ] Derniers fix & Publication - **Hellebore-jpg**