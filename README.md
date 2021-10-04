# Issue Tracking

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://img.shields.io)


Projet 10 de la formation DA Python de OpenClassrooms qui consiste à créer une API RESTFul en utilisant le framework Django Rest Framework, permettant de de créer des projets dans lesquels des utilisateurs (contributeurs) peuvent créer des problèmes et les commenter.  
La documentation de l'api est disponible [ici](https://documenter.getpostman.com/view/17717922/UUy1eSMZ#3406631b-c29f-4ffe-9a39-010ab4c84299)

## Pour commencer

- Télecharger le projet
- Aller dans le dossier du projet
- Créer un environnement virtuel : ``python3 -m venv env``
- Activer l'environnement virtuel : ``source env/bin/activate``
- Installer les packages : ``pip install -r requirements.txt``
- Générer une secret_key : [Djecrety](https://djecrety.ir/)
- Créer un fichier .env à la racine du projet et y mettre la clé généré dans une variable SECRET_KEY

## Démarrage

- Lancer le serveur : ``python manage.py runserver``
- Suivre la documentation de l'api pour connaître des diffèrentes requêtes possibles : [Documentation Issue Tracking](https://documenter.getpostman.com/view/17717922/UUy1eSMZ#3406631b-c29f-4ffe-9a39-010ab4c84299)

## Comptes utilisateurs test 

* Accès Admin :  
    - email : a@a.fr  
    - password : azerty

* Comptes utilisateur :  
    - username : moi@moi.fr
    - password : azerty

    - username : autre@autre.fr
    - password : azerty

## Fabriqué avec

* [Python 3](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django rest framework](https://www.django-rest-framework.org/)
