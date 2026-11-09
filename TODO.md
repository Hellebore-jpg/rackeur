# Historique des modifications et listes des objectifs

# 03/11/2026

## Organisation
- [x] Rôles dans le groupe - **Tout le monde**
    > `Hellebore-jpg` : Chef de projet
    > `chummel-ops` : Responsable de communication
- [x] Git & venv - **Hellebore-jpg**
    >- Création du repo Github et de la base.
    >- Ajout des collaborateurs : `Hellebore-jpg (Mathieu)` | `Purple-key-0 (Gabriel)` | `chummel-ops (Charles)` | `ylavallee-prog (Yanis)`
    >- Ajout de l'intervenant : `TheLegacy33`
    >- Explications du fonctionnement de venv à tout le monde et setup sur tout les PCs
    >- Création du .gitignore et de requirements.txt avec `pip freeze > requirements.txt`

## Objectifs
- [x] Répartition des rôles - **Tout le monde**
- [x] Création d'une Diréction Artistique + Logo + Nom d'app - **chummel-ops**
- [x] Script Python d'interaction CSV CRUD robuste
    - [x] 1ère affichage, en ligne de commande, de la liste des produits. ( R ) - **Hellebore-jpg**
    - [x] 1ère affichage, en ligne de commande, via une option, de la liste des produits, triés par nom, dans l'ordre alphabétique, et alphabétique inverse. ( R ) - **Hellebore-jpg**
    - [x] 1ère affichage, en ligne de commande, via une option, de la liste des produits, triés par prix, dans l'ordre croissant, et décroissant. ( R ) - **Hellebore-jpg**
    - [x] 1ère affichage, en ligne de commande, via une option, du ou des produits, en fonction d'un mot-clé (recherche d'un produit dans le catalogue). ( R ) - **Hellebore-jpg**
    - [x] Ajout, modification, et suppression d'un produit, en ligne de commande, via une ou plusieurs options. ( C U D ) - **Hellebore-jpg**
- [x] Création du Catalogue / Tableau de données - **Purple-key-0**
- [x] Relécture et analyse du Cahier des Charges - **chummel-ops** - **Purple-key-0**
- [x] Creation des taches du TODO.md - **chummel-ops**

## Autre
- [x] 1er livrable - **Tout le monde**

# 03/11/2026 + 

## -- Presentation -- 
- [ ] Canva de presentation de fin de projet . - **chummel-ops**
- [ ] Repartition de la parole pour la presentation. - **chummel-ops**
- [x] Rédaction du README.md - **Hellebore-jpg**

## -- Base de Données SQLite -- 
- [ ] Recherches, analyses, et synthèse autour du SGBD SQLite pour le passage CSV a SQLite. - **ylavallee-prog**
- [ ] Création manuelle du catalogue de produits sous la forme d’une table SQLite. ( Premeire BD SQLite ). - **ylavallee-prog**
- [ ] Passage du CSV a SQLite. - **ylavallee-prog**

## -- Authentification et Permision -- 
- [x] Définition de l'entité « utilisateur » avec prise en compte des différents rôles. - **Hellebore-jpg**
- [x] Création manuelle d'un jeu d'essais ( Données de tests ) dans la table « utilisateur ». - **Hellebore-jpg**
- [x] Implémentation du mécanisme d'authentification ( Code page connexion & inscription). - **Hellebore-jpg**
- [x] Hash des mots de passe en Bcrypt dans la base de données. - **Hellebore-jpg**
- [x] Gestion des autorisations, sur les 4 opérations sur le catalogue de produits, en ligne de commande, via une ou plusieurs options. - **Hellebore-jpg**
- [x] Implémentation de la création d'un nouvel utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer, au moyen de l'API RESTful « Have I Been Pwned », en ligne de commande, via une ou plusieurs options. - **Hellebore-jpg**

## -- Interface Utilisateur ( Recherche et Maquette ) --
- [x] Définition des sigles HMI, GUI, UI et UX. - **Hellebore-jpg**
    >- HMI (Human-Machine Interface) : Interface homme-machine, souvent industrielle, pour le contrôle de systèmes.
    >- GUI (Graphical User Interface) : Interface utilisateur graphique, axée sur les éléments visuels et graphiques.
    >- UI (User Interface) : Interface utilisateur, désignant les éléments visuels et interactifs d'un logiciel.
    >- UX (User Experience) : Expérience utilisateur, centrée sur la satisfaction et le parcours global de l'utilisateur.
- [ ] Recherches, analyses, et synthèse autour des solutions disponibles pour l'interfaçage utilisateur en Python. - **Purple-key-0** 
- [ ] Choix d'une solution pour l'interfaçage utilisateur de l'application de gestion du catalogue de produits.  - **chummel-ops**
- [ ] Maquette final des pages de l'aplication :
    - [x] Création d'un compte utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer. - **chummel-ops**
    - [x] Authentification.  - **chummel-ops**
    - [ ] Gestion de produits :
        - [ ] Affichage de la liste des produits, avec critères de tri. - **chummel-ops**
        - [ ] Recherche d'un produit en fonction d'un ou plusieurs mots-clés.  - **chummel-ops**
        - [ ] Ajout d'un produit.  - **chummel-ops**
        - [ ] Modification d'un produit. - **chummel-ops**
        - [ ] Suppression d'un produit. - **chummel-ops** 

## -- Interface Utilisateur ( Rendre fonctionelle ) -- 
- [ ] Implémentation des différents composants de l'interface utilisateur :
    - [ ] Création d'un compte utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer. - **Purple-key-0** 
    - [ ] Authentification. - **Purple-key-0** 
    - [ ] Gestion de produits :
        - [ ] Affichage de la liste des produits, avec critères de tri. - **Purple-key-0** 
        - [ ] Recherche d'un produit en fonction d'un ou plusieurs mots-clés. - **Purple-key-0** 
        - [ ] Ajout d'un produit. - **Purple-key-0** 
        - [ ] Modification d'un produit. - **Purple-key-0** 
        - [ ] Suppression d'un produit. - **Purple-key-0**  

## -- Bonus -- 
- [ ] Implémentation d'un système de notification ou d'alerte par envoi de mail en cas de nouveaux compromis détectés pour un utilisateur. - **chummel-ops** 
- [ ] Navigation par catégories dans l'interface
- [ ] Panel de gestion des utilisateurs admins et de leur permissions
- [ ] Jeu de données de test à installer optionellement pendant le setup de l'application - **Hellebore-jpg**
- [ ] Animations et autres améliorations graphiques
- [ ] Faux popup pour un "Abonnement Premium" gratuit
    - [ ] Interface Web
    - [ ] Base de données MySQL en ligne
    - [ ] Système de commandes des produits