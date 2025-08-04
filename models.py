# models.py

class Joueur:
    def __init__(self, nom, prenom, id_federation, sexe, classement):
        self.nom = nom
        self.prenom = prenom
        self.id_federation = id_federation
        self.sexe = sexe
        self.classement = classement

    def afficher(self):
        print("---- Joueur Details ----:")
        print(f"Nom: {self.nom}")
        print(f"Prénom: {self.prenom}")
        print(f"Fédération id: {self.id_federation}")
        print(f"Sexe: {self.sexe}")
        print(f"Classement: {self.classement}")

    def to_dict(self): #to_dict() → transforme le joueur en dictionnaire compatible avec JSON.
        """Convertit le joueur en dictionnaire pour l'enregistrement JSON."""
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "id_federation": self.id_federation,
            "sexe": self.sexe,
            "classement": self.classement
        }

    @classmethod
    def from_dict(cls, data): #from_dict() → méthode de classe qui recrée un joueur à partir d’un dictionnaire JSON.
        """Crée un joueur à partir d’un dictionnaire JSON."""
        return cls(
            nom=data["nom"],
            prenom=data["prenom"],
            id_federation=data["id_federation"],
            sexe=data["sexe"],
            classement=data["classement"]
        )


class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, nombre_de_rondes=4, description=""):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_de_rondes = nombre_de_rondes
        self.description = description
        self.joueurs = []
        self.rondes = []

    def __str__(self):
        return (f"Tournoi: {self.nom}\n"
                f"Lieu: {self.lieu}\n"
                f"Date de debut: {self.date_debut}\n"
                f"Date de fin: {self.date_fin}\n"
                f"Nombre de rondes: {self.nombre_de_rondes}\n"
                f"Description: {self.description}")
    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nombre_de_rondes": self.nombre_de_rondes,
            "description": self.description,
            "joueurs": [j.to_dict() for j in self.joueurs],
            "rondes": [r.to_dict() for r in self.rondes]
        }

    @classmethod
    def from_dict(cls, data):
        tournoi = cls(
            nom=data["nom"],
            lieu=data["lieu"],
            date_debut=data["date_debut"],
            date_fin=data["date_fin"],
            nombre_de_rondes=data.get("nombre_de_rondes", 4),
            description=data.get("description", "")
        )
        tournoi.joueurs = [Joueur.from_dict(j) for j in data.get("joueurs", [])]
        tournoi.rondes = [Ronde.from_dict(r) for r in data.get("rondes", [])]
        return tournoi


class Match:
    def __init__(self, joueur1, joueur2, score1=0, score2=0):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = score1
        self.score2 = score2

    def __str__(self):
        return (f"{self.joueur1.nom} vs {self.joueur2.nom} => Score: {self.score1} - {self.score2}")
   
    def to_dict(self):
        return {
            "joueur1": self.joueur1.to_dict(),
            "joueur2": self.joueur2.to_dict(),
            "score1": self.score1,
            "score2": self.score2
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            joueur1=Joueur.from_dict(data["joueur1"]),
            joueur2=Joueur.from_dict(data["joueur2"]),
            score1=data["score1"],
            score2=data["score2"]
        )


class Ronde:
    def __init__(self, numero, matchs=None):
        self.numero = numero
        self.matchs = matchs if matchs is not None else []

    def ajouter_match(self, match):
        self.matchs.append(match)

    def __str__(self):
        resultat = f"Ronde {self.numero}:\n"
        for match in self.matchs:
            resultat += f"  {match}\n"
        return resultat
    def to_dict(self):
        return {
            "numero": self.numero,
            "matchs": [m.to_dict() for m in self.matchs]
        }

    @classmethod
    def from_dict(cls, data):
        matchs = [Match.from_dict(m) for m in data["matchs"]]
        return cls(numero=data["numero"], matchs=matchs)
