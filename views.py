# views.py

def afficher_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Créer un joueur")
    print("2. Créer un tournoi")
    print("3. Afficher les détails du tournoi")
    print("4. Tester un match et une ronde")
    print("5. Sauvegarder les joueurs")
    print("6. Charger les joueurs depuis un fichier")
    print("7. Sauvegarder le tournoi")
    print("8. Charger un tournoi depuis un fichier ")
    print("9. Afficher la liste des joueurs")
    print("10. Quitter")


def afficher_tournoi(tournoi):
    print("\n--- Détails du tournoi ---")
    print(f"Nom : {tournoi.nom}")
    print(f"Lieu : {tournoi.lieu}")
    print(f"Date de début : {tournoi.date_debut}")
    print(f"Date de fin : {tournoi.date_fin}")
    print(f"Nombre de rondes prévues : {tournoi.nombre_de_rondes}")
    print(f"Description : {tournoi.description}")
    #print(f"Nombre de joueurs inscrits : {len(tournoi.joueurs)}")
    #print(f"Nombre de rondes jouées : {len(tournoi.rondes)}")

def afficher_match(match):
    print(f"Match: {match.joueur1.nom} vs {match.joueur2.nom}")
    print(f"Score: {match.score1} - {match.score2}")

def afficher_ronde(ronde):
    print(f"\n--- Ronde {ronde.numero} ---")
    for i, match in enumerate(ronde.matchs, start=1):
        print(f"Match {i}:")
        afficher_match(match)
        print("-" * 20)


