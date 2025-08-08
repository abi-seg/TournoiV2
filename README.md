# Gestionnaire de Tournoi d’Échecs

Un programme Python pour gérer des tournois d’échecs en club, basé sur l’architecture Modèle-Vue-Contrôleur (MVC).

## Fonctionnalités

- Création et gestion des joueurs
- Création et gestion des tournois
- Sélection des joueurs pour chaque tournoi
- Génération automatique des appariements 
- Saisie des résultats de chaque match
- Calcul et affichage du classement
- Sauvegarde et chargement des données au format JSON
- Fonctionne entièrement hors ligne

## Prérequis

- Python 3.7 ou version supérieure

## Installation

1. Clonez ce dépôt :
   git clone https://github.com/abi-seg/TournoiV2.git
   cd TournoiV2
   
2. (Optionnel) Créez un environnement virtuel :
    python -m venv venv
    source venv/bin/activate  # Sous Windows : venv\Scripts\activate
   

## Utilisation

Lancez le programme principal :
python main.py

Un menu s’affichera avec les options suivantes :

Créer un joueur
Sauvegarder les joueurs
Afficher la liste des joueurs
Charger les joueurs depuis un fichier
Créer un tournoi
Sauvegarder le tournoi
Afficher les détails du tournoi
Charger un tournoi depuis un fichier
Démarrer un nouveau tour
Entrer les résultats du tour en cours
Afficher le classement du tournoi
Afficher tous les tours et résultats
Quitter
Toutes les données sont enregistrées dans des fichiers JSON (joueurs.json et tournois.json) dans le dossier du projet.

## Structure du code

models.py — Classes pour les joueurs, tournois, rondes et matchs
views.py — Fonctions d’affichage pour l’utilisateur
controller.py — Logique principale et gestion du menu
main.py — Point d’entrée du programme

## Pour vérifier la conformité du code avec la PEP 8 :
pip install flake8
flake8 --format=html --htmldir=flake-report

Pour toute question ou remarque, vous pouvez me contacter [abirami1488@gmail.com]
