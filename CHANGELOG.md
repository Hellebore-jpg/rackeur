# Changelog

Toutes les modifications notables apportées à ce projet sont documentées dans ce fichier.

Ce projet suit les conventions de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et utilise le versionnage sémantique ([Semantic Versioning](https://semver.org/lang/fr/)).

## [Non publié]

### Prévu
- Navigation par catégories dans l'interface.
- Création et gestion du profil utilisateur.
- Mise en place d'un système de commandes.
- Consultation de l'historique des commandes.

---

## [1.0.0] - 13/11/2026

Première version stable de Rackeur.

### Ajouté

#### Interface utilisateur
- Création de l'identité visuelle de Rackeur : direction artistique, logo et nom de l'application.
- Conception et intégration des interfaces graphiques avec PyQt6.
- Création des interfaces de connexion et d'inscription.
- Mise en place d'un catalogue de produits avec affichage et tri.
- Ajout d'un système de recherche par mots-clés.
- Création des interfaces d'ajout, de modification et de suppression de produits.
- Mise en place d'un panneau d'administration pour la gestion des utilisateurs et de leurs permissions.

#### Gestion du catalogue
- Implémentation des opérations CRUD (Create, Read, Update, Delete) sur les produits.
- Affichage et tri des produits par ordre alphabétique et par prix.
- Ajout de la recherche de produits par mots-clés.
- Ajout de la recherche par catégories.
- Gestion des autorisations associées aux opérations sur le catalogue.

#### Gestion des utilisateurs
- Mise en place d'un système d'inscription et d'authentification.
- Création de plusieurs rôles utilisateurs : visiteur, utilisateur, éditeur et administrateur.
- Gestion des permissions selon les rôles et les autorisations attribuées.
- Ajout d'un système de notification en cas de détection de nouveaux mots de passe compromis.

#### Bases de données
- Première implémentation du stockage des données au format CSV.
- Migration et prise en charge du stockage au format SQLite.
- Possibilité de choisir le format de base de données au démarrage de l'application.
- Création des scripts d'interaction avec les bases de données CSV et SQLite.
- Ajout de jeux de données de démonstration pour les produits et les utilisateurs.

### Sécurité
- Mise en application du principe du moindre privilège (*Principle of Least Privilege*, PoLP).
- Hachage des mots de passe avec bcrypt avant leur stockage en base de données.
- Intégration de l'API Have I Been Pwned pour détecter les mots de passe compromis.
- Vérification des mots de passe lors de l'inscription et proposition de suggestions pour les renforcer.
- Détection des nouveaux compromis affectant les mots de passe des utilisateurs.
- Mise en place d'un système de permissions pour limiter l'accès aux fonctionnalités sensibles.

### Documentation
- Création du README.md et rédaction des instructions d'installation.
- Création et organisation du TODO.md pour le suivi du développement.
- Documentation du code Python à l'aide de commentaires et d'annotations de types.
- Réalisation d'un support de présentation du projet.

### Compilation et publication
- Création d'un exécutable autonome pour Windows avec Nuitka.
- Création d'un exécutable autonome pour Linux avec Nuitka.
- Ajout des fichiers de bases de données au .gitignore.
- Préparation et publication de la version 1.0.0 sur GitHub.

---

[Non publié]: https://github.com/Hellebore-jpg/rackeur/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Hellebore-jpg/rackeur/releases/tag/v1.0.0