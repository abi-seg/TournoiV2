# views.py

def afficher_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Créer un joueur")
    print("2. Sauvegarder les joueurs")
    print("3. Afficher la liste des joueurs")
    print("4. Charger les joueurs depuis un fichier")
    print("5. Créer un tournoi")
    print("6. Sauvegarder le tournoi")
    print("7. Afficher les détails du tournoi")
    print("8. Charger un tournoi depuis un fichier")
    print("9. Démarrer un nouveau tour")
    print("10. Entrer les résultats du tour en cours")
    print("11. Afficher le classement du tournoi")
    print("12. Afficher tous les tours et résultats")
    print("13. Quitter")


def afficher_tournoi(tournoi):
    print("\n--- Détails du tournoi ---")
    print(f"Nom : {tournoi.nom}")
    print(f"Lieu : {tournoi.lieu}")
    print(f"Date de début : {tournoi.date_debut}")
    print(f"Date de fin : {tournoi.date_fin}")
    print(f"Nombre de rondes prévues : {tournoi.nombre_de_rondes}")
    print(f"Description : {tournoi.description}")
    #afficher les joueurs du tournoi
    if tournoi.joueurs:
        print("\n Joueurs inscrits dans ce tournoi : ")
        for idx, joueur in enumerate(sorted(tournoi.joueurs, key=lambda j: (j.nom,j.prenom)), start = 1):
            print(f"{idx}.{joueur.nom} {joueur.prenom} (ID: {joueur.id_federation}, Classement: {joueur.classement})")
    else:
        print("Aucun joueur inscrit dans ce tournoi.")

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

def afficher_tous_les_tours(tournoi):
    if not tournoi or not tournoi.rondes:
        print("Aucun tour n'a encore été joué pour ce tournoi.")
        return
    print(f"\n--- Tous les tours du tournoi : {tournoi.nom} ---")
    for ronde in tournoi.rondes:
        print(ronde)
