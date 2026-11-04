# Historique des modifications et listes des objectifs

# 03/11/2026

## Organisation
- [x] Rôles dans le groupe - **Tout le monde**
    >`Hellebore-jpg` : 
    >`Purple-key-0` : 
    >`chummel-ops` : 
    >`ylavallee-prog` : 
- [x] Git & venv - **Hellebore-jpg** :
    >- Création du repo Github et de la base.
    >- Ajout des collaborateurs : `Hellebore-jpg (Mathieu)` | `Purple-key-0 (Gabriel)` | `chummel-ops (Charles)` | `ylavallee-prog (Yanis)`
    >- Ajout de l'intervenant : `TheLegacy33`
    >- Explications du fonctionnement de venv à tout le monde et setup sur tout les PCs

## Objectifs
- [ ] Taches du premier jour : 
    -  [x] Répartition des rôles  - **Tout le monde**
        > `Hellebore-jpg` : Chef de projet
        > `chummel-ops` : Responsable de communication
    -  [x] Création d'un Diréction Artistique + Logo + Nom d'app  - **chummel-ops**
    -  [x] Classe Python interaction avec le CSV  - **Hellebore-jpg**
    -  [x] Création du Catalogue / Tableau de données - **Purple-key-0** 
    -  [x] Relécture et analyse du Cahier des Charges  - **chummel-ops** + **Purple-key-0**
    -  [x] Creation des taches du TODO.md  - **chummel-ops** 

## Autre
- [ ] 1er livrable - **Tout le monde**

# 03/11/2026 + 

## -- CRUD ( Pour le tableau CSV ) --
- [ ] 1ère affichage, en ligne de commande, de la liste des produits.( R ) - **Hellebore-jpg**
- [ ] 1ère affichage, en ligne de commande, via une option, de la liste des  produits, triés par nom, dans l’ordre alphabétique, et alphabétique inverse. ( R ) - **Hellebore-jpg**
- [ ] 1ère affichage, en ligne de commande, via une option, de la liste des  produits, triés par prix, dans l’ordre croissant, et décroissant. ( R ) - **Hellebore-jpg**
- [ ] 1ère affichage, en ligne de commande, via une option, du ou des produits,  en fonction d’un mot-clé (recherche d’un produit dans le catalogue). ( R ) - **Hellebore-jpg**
- [ ] Ajout, modification, et suppression d’un produit, en ligne de
commande, via une ou plusieurs options. ( C U D ) - **Hellebore-jpg**

## -- Presentation -- 
- [ ] Canva de presentation de fin de projet . - **chummel-ops** 
- [ ] Repartition de la parole pour la presentation. - **chummel-ops** 

## -- BD SQLite -- 
- [ ] Recherches, analyses, et synthèse autour du SGBD SQLite pour le passage CSV a SQLite. - **ylavallee-prog**
- [ ] Création manuelle du catalogue de produits sous la forme d’une table SQLite.( Premeire BD SQLite ). - **ylavallee-prog**

## -- Authentification et Permision -- 
- [ ] Définition de l'entité « utilisateur » avec prise en compte des différents rôles. - **Hellebore-jpg**
- [x] Création manuelle d’un jeu d’essais dans la table « utilisateur ».( Données de tests )  - **Hellebore-jpg**
- [ ] Implémentation du mécanisme d’authentification ( Code page connexion).  - **Hellebore-jpg**
- [ ] Gestion des autorisations, sur les 4 opérations sur le catalogue de produits, en ligne de commande, via une ou plusieurs options.  - **Hellebore-jpg**

## -- Securité des Mots Passes 
- [ ] Implémentation de la création d’un nouvel utilisateur avec détection
de mots de passe compromis et proposition de suggestions pour les
renforcer, en ligne de commande, via une ou plusieurs options.
- [ ] Implémentation de la création d’un nouvel utilisateur avec détection
de mots de passe compromis et proposition de suggestions pour les
renforcer, au moyen de l’API RESTful « Have I Been Pwned », en ligne
de commande, via une ou plusieurs options.
- [ ] Définition des sigles HMI, GUI, UI et UX.

## -- Interface Utilisateur ( Recherche et Maquette )
- [ ] Recherches, analyses, et synthèse autour des solutions disponibles
pour l'interfaçage utilisateur en Python. - **Purple-key-0** 
- [ ] Choix d’une solution pour l'interfaçage utilisateur de l’application de
gestion du catalogue de produits.  - **chummel-ops**
- [ ] Maquette final des pages de l'aplication :
    - [ ] Création d’un compte utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer.  - **chummel-ops**
    - [ ] Authentification.  - **chummel-ops**
    - [ ] Gestion de produits :
        - [ ] Affichage de la liste des produits, avec critères de tri.  - **chummel-ops**
        - [ ] Recherche d’un produit en fonction d’un ou plusieurs mots-clés.  - **chummel-ops**
        - [ ] Ajout d’un produit.  - **chummel-ops**
        - [ ] Modification d’un produit.  - **chummel-ops**
        - [ ] Suppression d’un produit.  - **chummel-ops** 

## -- Interface Utilisateur ( Rendre fonctionelle ) -- 
- [ ] Implémentation des différents composants de l’interface utilisateur :
    - [ ] Création d’un compte utilisateur avec détection de mots de passe compromis et proposition de suggestions pour les renforcer. - **Purple-key-0** 
    - [ ] Authentification. - **Purple-key-0** 
    - [ ] Gestion de produits :
        - [ ] Affichage de la liste des produits, avec critères de tri. - **Purple-key-0** 
        - [ ] Recherche d’un produit en fonction d’un ou plusieurs mots-clés. - **Purple-key-0** 
        - [ ] Ajout d’un produit. - **Purple-key-0** 
        - [ ] Modification d’un produit. - **Purple-key-0** 
        - [ ] Suppression d’un produit. - **Purple-key-0**  

## -- Bonus -- 
- [ ] Implémentation d’un système de notification ou d'alerte par envoi de mail en cas de nouveaux compromis détectés pour un utilisateur. - **chummel-ops** 
