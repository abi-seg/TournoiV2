# controller.py
import json
from models import Joueur, Tournoi, Match, Ronde
from views import afficher_menu, afficher_tournoi, afficher_match, afficher_ronde

def sauvegarder_tous_les_tournois(liste_tournois, chemin_fichier="tournois.json"):
    data = [t.to_dict() for t in liste_tournois]
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
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
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Joueurs sauvegardés dans {nom_fichier}")


def charger_joueurs(nom_fichier="joueurs.json"):
    liste_joueurs = []
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                joueur = Joueur(item["nom"], item["prenom"], item["id_federation"], item["sexe"], item["classement"])
                liste_joueurs.append(joueur)
       
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

def joueur_existe(joueurs,nom,prenom,id_federation):
    for joueur in joueurs:
        if(joueur.nom==nom and
           joueur.prenom==prenom and
           joueur.id_federation==id_federation):
           return True
    return False


def creer_joueur(joueurs):
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
    if joueur_existe(joueurs,nom,prenom,id_federation):
        print("Ce joueur existe déjà dans la liste!")
        return None
    return Joueur(nom, prenom, id_federation, sexe, classement)

def creer_tournoi():
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
    return Tournoi(nom, lieu, date_debut, date_fin, nombre_de_rondes, description)

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
    global tournois,joueurs
    tournoi = None
    print("Bienvenue dans le gestionnaire de tournoi !")
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-10) : ")

        if choix == "1":
            joueur = creer_joueur(joueurs)
            if joueur:
                joueurs.append(joueur)
                print("Joueur créé avec succès !")
                joueur.afficher()

        elif choix == "2":
            tournoi = creer_tournoi()
            tournois.append(tournoi)
            print("Tournoi créé avec succès !")

        elif choix == "3":
            if tournois:
                print("\n Détails de tous les tournois enregistrés:")
                for idx, t in enumerate(tournois, start=1):
                    print(f"\n Tournoi {idx} :")
                    afficher_tournoi(t)
            else:
                print("Aucun tournoi n’a encore été créé.")

        elif choix == "4":
            tester_match_et_ronde_dynamique(joueurs)

        elif choix == "5":
            sauvegarder_joueurs(joueurs)

        elif choix == "6":
            print("Les joueurs sont déjà chargés automatiquement au démarrage.")
            print("Utilisez l'option 5 pour sauvegarder les nouveaux joueurs.")

        elif choix == "7":
            if tournois:
                sauvegarder_tous_les_tournois(tournois)
                
            else:
                print("Aucun tournoi à sauvegarder.")

        elif choix == "8":
            tournois = charger_tournois()  # Refresh from file
            if tournois:
                print("\n Liste des tournois disponibles :")
                for idx, t in enumerate(tournois, start=1):
                    print(f"{idx}. {t.nom} ({t.lieu}, du {t.date_debut} au {t.date_fin})")

                try:
                    selection = int(input("Entrez le numéro du tournoi à afficher : "))
                    if 1 <= selection <= len(tournois):
                        tournoi = tournois[selection - 1]
                        print(f"\n Tournoi sélectionné : {tournoi.nom}")
                        afficher_tournoi(tournoi)
                    else:
                        print(" Numéro invalide.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un numéro entier.")
            else:
                print("Aucun tournoi enregistré.")

        elif choix == "9":
            if joueurs:
                print("\nListe des joueurs enregistrés :")
                for idx, joueur in enumerate(joueurs, start=1):
                    print(f"\nJoueur {idx} : ")
                    joueur.afficher()
            else:
                print("Aucun joueur à afficher.")

        elif choix == "10":
            print("Au revoir !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

