# controller.py
import os
import json
from models import Joueur, Tournoi, Match, Ronde
from views import afficher_menu, afficher_tournoi, afficher_match, afficher_ronde, afficher_tous_les_tours
""""
def sauvegarder_tournoi(tournoi, chemin_fichier="tournois.json"):
    
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(tournoi.to_dict())

    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Tournoi ajouté à {chemin_fichier}")
"""
def sauvegarder_tous_les_tournois(liste_tournois, chemin_fichier="tournois.json"):
    data = [t.to_dict() for t in liste_tournois]
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Tous les tournois sauvegardés dans {chemin_fichier}")

def sauvegarder_joueurs(liste_joueurs, nom_fichier="joueurs.json"):
    data = []
    for joueur in liste_joueurs:
        data.append({
            "nom": joueur.nom,
            "prenom": joueur.prenom,
            "id_federation": joueur.id_federation,
            "sexe": joueur.sexe,
            "classement": joueur.classement
        })
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Joueurs sauvegardés dans {nom_fichier}")


def charger_joueurs(nom_fichier="joueurs.json"):
    liste_joueurs = []
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                joueur = Joueur(item["nom"], item["prenom"], item["id_federation"], item["sexe"], item["classement"])
                liste_joueurs.append(joueur)
        #print(f"{len(liste_joueurs)} joueurs chargés depuis {nom_fichier}")
    except FileNotFoundError:
        print("Aucun fichier de joueurs trouvé. Liste vide initialisée.")
    return liste_joueurs


def charger_tournois(chemin_fichier="tournois.json"):
    """Charge tous les tournois depuis le fichier JSON."""
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            return[Tournoi.from_dict(t) for t in data]
            
    except FileNotFoundError:
        print("Fichier non trouvé.")
        return []



def creer_joueur():
    nom = input("Entrez le nom: ")
    prenom = input("Entrez le prénom: ")
    id_federation = input("Entrez l'identifiant fédération: ")
    sexe = input("Entrez le sexe (m/f): ")
    classement = input("Entrez le classement (entier): ")
    try:
        classement = int(classement)
    except ValueError:
        print("Classement invalide, mis à 0 par défaut.")
        classement = 0
    return Joueur(nom, prenom, id_federation, sexe, classement)

def creer_tournoi(joueurs):
    nom = input("Nom du tournoi : ")
    lieu = input("Lieu du tournoi : ")
    date_debut = input("Date de début (AAAA-MM-JJ) : ")
    date_fin = input("Date de fin (AAAA-MM-JJ) : ")
    try:
        nombre_de_rondes = int(input("Nombre de rondes (défaut = 4) : ") or 4)
        if nombre_de_rondes !=4:
            print("Seules 4 rondes sont autorisées.")
            nombre_de_rondes = 4
    except ValueError:
        print("Valeur invalide, nombre de rondes mis à 4.")
        
    description = input("Description (optionnelle) : ")
    tournoi = Tournoi(nom, lieu, date_debut, date_fin, nombre_de_rondes, description)
    #-------select players for the tournament-----
    print("\n Sélectionnez les joueurs à ajouter au tournoi(enterez les numéros séparés par des virgules):")
    for idx, joueur in enumerate(joueurs, start=1):
       print(f"{idx}.{joueur.nom} {joueur.prenom}")
    selections = input("Numéros des joueurs : ")
    try:
        indices=[int(s.strip()) - 1 for s in selections.split(",")]
        for idx in indices:
            if 0<=idx<len(joueurs):
                tournoi.joueurs.append(joueurs[idx])
        print("Joueurs ajoutés au tournoi.")
    except Exception as e:
        print("Erreur lors de la sélection des joueurs : ",e)
    return tournoi
"""""
def tester_match_et_ronde():
    joueur1 = Joueur("Alice", "Durand", "FR001", "f", 1600)
    joueur2 = Joueur("Bob", "Martin", "FR002", "m", 1550)
    match = Match(joueur1, joueur2, score1=1, score2=0)
    print("\n ----- Affichage Match ------")
    afficher_match(match)
    ronde = Ronde(1)
    ronde.ajouter_match(match)
    afficher_ronde(ronde)
"""
import random

def generate_first_round_pairs(joueurs):
    joueurs_copy = joueurs[:]
    random.shuffle(joueurs_copy)
    pairs = []
    for i in range(0, len(joueurs_copy), 2):
        joueur1 = joueurs_copy[i]
        joueur2 = joueurs_copy[i+1]
        pairs.append(([joueur1, 0], [joueur2, 0]))
    return pairs

def get_previous_matches(tournoi):
    previous_matches = set()
    for ronde in tournoi.rondes:
        for match in ronde.matchs:
            key = frozenset([match[0][0].id_federation, match[1][0].id_federation])
            previous_matches.add(key)
    return previous_matches

def generate_next_round_pairs(joueurs, previous_matches):
    joueurs_sorted = sorted(joueurs, key=lambda j: j.points, reverse=True)
    pairs = []
    used = set()
    i = 0
    while i < len(joueurs_sorted) - 1:
        j1 = joueurs_sorted[i]
        for j in range(i+1, len(joueurs_sorted)):
            j2 = joueurs_sorted[j]
            key = frozenset([j1.id_federation, j2.id_federation])
            if key not in previous_matches and j2 not in used:
                pairs.append(([j1, 0], [j2, 0]))
                used.add(j1)
                used.add(j2)
                previous_matches.add(key)
                break
        i += 1
        while i < len(joueurs_sorted) and joueurs_sorted[i] in used:
            i += 1
    return pairs
def start_new_round(tournoi):
    if not tournoi.rondes:
        pairs = generate_first_round_pairs(tournoi.joueurs)
    else:
        previous_matches = get_previous_matches(tournoi)
        pairs = generate_next_round_pairs(tournoi.joueurs, previous_matches)
    
    round_number = len(tournoi.rondes) + 1
    ronde = Ronde(round_number)
    for pair in pairs:
        joueur1, _ = pair[0]
        joueur2, _ = pair[1]
        ronde.ajouter_match(joueur1, joueur2)
    tournoi.rondes.append(ronde)
    tournoi.current_round_number = round_number
    print(f"{ronde.name} started with the following pairings:")
    print(ronde)
    return ronde
def enter_results_for_round(ronde):
    for idx, match in enumerate(ronde.matchs):
        joueur1, _ = match[0]
        joueur2, _ = match[1]
        print(f"Match {idx+1}: {joueur1.nom} vs {joueur2.nom}")
        try:
            score1 = float(input(f"Score for {joueur1.nom}: "))
            score2 = float(input(f"Score for {joueur2.nom}: "))
        except ValueError:
            print("Invalid input, setting scores to 0.")
            score1, score2 = 0, 0
        ronde.entrer_resultat(idx, score1, score2)

def update_player_points(ronde):
    for match in ronde.matchs:
        joueur1, score1 = match[0]
        joueur2, score2 = match[1]
        joueur1.points += score1
        joueur2.points += score2


def tester_match_et_ronde_dynamique(joueurs):
    if len(joueurs) < 2:
        print("Il faut au moins deux joueurs pour créer un match.")
        return

    print("\nSélectionnez les joueurs pour le match :")
    for idx, joueur in enumerate(joueurs, start=1):#to get index and it's value enumerate is used
        print(f"{idx}. {joueur.nom} {joueur.prenom}")

    try:
        idx1 = int(input("Numéro du premier joueur : ")) - 1 #On soustrait 1 pour passer d'une numérotation "humaine" (qui commence à 1) 
                                                             #à une numérotation Python (qui commence à 0).
        idx2 = int(input("Numéro du second joueur : ")) - 1
        if idx1 == idx2 or idx1 not in range(len(joueurs)) or idx2 not in range(len(joueurs)):
            print("Sélection invalide.")
            return
    except ValueError:
        print("Entrée invalide.")
        return

    try:
        score1 = float(input(f"Score pour {joueurs[idx1].nom} {joueurs[idx1].prenom} : "))
        score2 = float(input(f"Score pour {joueurs[idx2].nom} {joueurs[idx2].prenom} : "))
    except ValueError:
        print("Scores invalides, mis à 0 par défaut.")
        score1 = 0
        score2 = 0

    match = Match(joueurs[idx1], joueurs[idx2], score1, score2)
    ronde = Ronde(1)
    ronde.ajouter_match(match)
    print("\n----- Affichage Match ------")
    afficher_match(match)
    afficher_ronde(ronde)
    
# Charger les joueurs sauvegardés dès le lancement
joueurs = charger_joueurs()
tournois = charger_tournois()

def menu_principal():
    global tournois, joueurs
    tournoi = None
    print("Bienvenue dans le gestionnaire de tournoi !")
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-13) : ").strip()

        if choix == "1":
            joueur = creer_joueur()
            joueurs.append(joueur)
            print("Joueur créé avec succès !")
            joueur.afficher()

        elif choix == "2":
            sauvegarder_joueurs(joueurs)

        elif choix == "3":
            if joueurs:
                print("\nListe des joueurs enregistrés :")
                for idx, joueur in enumerate(joueurs, start=1):
                    print(f"\nJoueur {idx} : ")
                    joueur.afficher()
            else:
                print("Aucun joueur à afficher.")

        elif choix == "4":
            joueurs = charger_joueurs()
            print("Joueurs rechargés depuis le fichier.")

        elif choix == "5":
            tournoi = creer_tournoi(joueurs)
            tournois.append(tournoi)
            print("Tournoi créé avec succès !")

        elif choix == "6":
            if tournois:
                sauvegarder_tous_les_tournois(tournois)
            else:
                print("Aucun tournoi à sauvegarder.")

        elif choix == "7":
            if tournois:
                print("\nDétails de tous les tournois enregistrés:")
                for idx, t in enumerate(tournois, start=1):
                    print(f"\nTournoi {idx} :")
                    afficher_tournoi(t)
            else:
                print("Aucun tournoi n’a encore été créé.")

        elif choix == "8":
            tournois = charger_tournois()
            print("Tournois rechargés depuis le fichier.")

        elif choix == "9":
            if tournois:
                for idx, t in enumerate(tournois, start=1):
                    print(f"{idx}. {t.nom}")
                selection = int(input("Sélectionnez le tournoi : "))
                if 1 <= selection <= len(tournois):
                    tournoi = tournois[selection - 1]
                    ronde = start_new_round(tournoi)
                else:
                    print("Numéro invalide.")
            else:
                print("Aucun tournoi disponible.")

        elif choix == "10":
            if tournoi and tournoi.rondes:
                ronde = tournoi.rondes[-1]
                enter_results_for_round(ronde)
                update_player_points(ronde)
                ronde.terminer()
                print(f"{ronde.name} terminé.")
            else:
                print("Aucun tour en cours pour ce tournoi.")

        elif choix == "11":
            if tournoi:
                print("\nClassement du tournoi :")
                classement = sorted(tournoi.joueurs, key=lambda j: j.points, reverse=True)
                for idx, joueur in enumerate(classement, start=1):
                    print(f"{idx}. {joueur.nom} {joueur.prenom} - {joueur.points} points")
            else:
                print("Aucun tournoi sélectionné.")
        elif choix == "12":
            if tournoi:
                afficher_tous_les_tours(tournoi)
            else:
                print("Aucun tournoi selectionné")

        elif choix == "13":
            print("Au revoir !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

