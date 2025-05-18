import json

def charger_donnees(fichier):
    
   
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            bibliotheque = json.load(f)
            if isinstance(bibliotheque, list):
                return bibliotheque
            else:
                return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def sauvegarder_donnees(bibliotheque, fichier):
    try:
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(bibliotheque, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")

def generer_id(bibliotheque):
    if not bibliotheque:
        return 1
    else:
        max_id = max(livre["ID"] for livre in bibliotheque)
        return max_id + 1

def afficher_tous_les_livres(bibliotheque):
    if not bibliotheque:
        print("Aucun livre dans la bibliothèque.")
        return
    print("\nListe complète des livres :")
    for livre in bibliotheque:
        id_livre = livre["ID"]
        titre = livre["Titre"]
        auteur = livre["Auteur"]
        annee = livre["Année"]
        lu = livre["Lu"]
        note = livre.get("Note", None)
        commentaire = livre.get("Commentaire", None)
        lu_str = "Oui" if lu else "Non"
        ligne = f"ID {id_livre} : \"{titre}\" par {auteur} ({annee}) - Lu : {lu_str}"
        if lu and note is not None:
            ligne += f", Note : {note}/10"
        print(ligne)
        if lu and commentaire:
            print(f"    Commentaire : {commentaire}")
    print() 

def ajouter_livre(bibliotheque):
    print("\n*** Ajouter un nouveau livre ***")
    titre = input("Titre du livre : ").strip()
    if titre == "":
        print("Le titre ne peut pas être vide. Ajout annulé.")
        return
    auteur = input("Auteur du livre : ").strip()
    if auteur == "":
        print("L'auteur ne peut pas être vide. Ajout annulé.")
        return
    annee_str = input("Année de publication : ").strip()
    if annee_str == "":
        print("L'année ne peut pas être vide. Ajout annulé.")
        return
    try:
        annee = int(annee_str)
    except ValueError:
        print("Année invalide. Ajout annulé.")
        return
    new_id = generer_id(bibliotheque)
    nouveau_livre = {
        "ID": new_id,
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None,
        "Commentaire": None
    }
    bibliotheque.append(nouveau_livre)
    print(f"Livre ajouté avec succès (ID {new_id}).")

def supprimer_livre(bibliotheque):
    print("\n*** Supprimer un livre ***")
    id_str = input("Entrez l'ID du livre à supprimer : ").strip()
    if id_str == "":
        print("Opération annulée (aucun ID fourni).")
        return
    try:
        id_livre = int(id_str)
    except ValueError:
        print("ID invalide. Veuillez entrer un nombre.")
        return
    # Recherche du livre avec l'ID fourni
    livre_a_supprimer = next((livre for livre in bibliotheque if livre["ID"] == id_livre), None)
    if livre_a_supprimer is None:
        print(f"Aucun livre avec l'ID {id_livre} n'a été trouvé.")
        return
    confirmation = input(f"Êtes-vous sûr de vouloir supprimer \"{livre_a_supprimer['Titre']}\" ? (O/N) : ")
    if confirmation.lower() == 'o':
        bibliotheque.remove(livre_a_supprimer)
        print("Livre supprimé avec succès.")
    else:
        print("Suppression annulée.")

def rechercher_livre(bibliotheque):
    print("\n*** Rechercher un livre ***")
    mot_cle = input("Entrez un mot-clé pour la recherche : ").strip()
    if mot_cle == "":
        print("Opération annulée (mot-clé vide).")
        return
    mot_cle_lower = mot_cle.lower()
    resultats = [livre for livre in bibliotheque 
                 if mot_cle_lower in livre["Titre"].lower() or mot_cle_lower in livre["Auteur"].lower()]
    if not resultats:
        print(f"Aucun livre trouvé pour le mot-clé \"{mot_cle}\".")
    else:
        print(f"{len(resultats)} livre(s) trouvé(s) pour \"{mot_cle}\" :")
        for livre in resultats:
            id_livre = livre["ID"]
            titre = livre["Titre"]
            auteur = livre["Auteur"]
            annee = livre["Année"]
            lu = livre["Lu"]
            note = livre.get("Note", None)
            commentaire = livre.get("Commentaire", None)
            lu_str = "Oui" if lu else "Non"
            ligne = f"ID {id_livre} : \"{titre}\" par {auteur} ({annee}) - Lu : {lu_str}"
            if lu and note is not None:
                ligne += f", Note : {note}/10"
            print(ligne)
            if lu and commentaire:
                print(f"    Commentaire : {commentaire}")

def marquer_comme_lu(bibliotheque):
    print("\n*** Marquer un livre comme lu ***")
    id_str = input("Entrez l'ID du livre à marquer comme lu : ").strip()
    if id_str == "":
        print("Opération annulée (aucun ID fourni).")
        return
    try:
        id_livre = int(id_str)
    except ValueError:
        print("ID invalide. Veuillez entrer un nombre.")
        return
    livre_trouve = next((livre for livre in bibliotheque if livre["ID"] == id_livre), None)
    if livre_trouve is None:
        print(f"Aucun livre avec l'ID {id_livre} n'a été trouvé.")
        return
    if livre_trouve["Lu"]:
        confirm = input("Ce livre est déjà marqué comme lu. Mettre à jour la note/commentaire ? (O/N) : ")
        if confirm.lower() != 'o':
            print("Opération annulée.")
            return
    livre_trouve["Lu"] = True
    note_str = input("Entrez une note sur 10 (laissez vide pour aucune note) : ").strip()
    if note_str == "":
        livre_trouve["Note"] = None
    else:
        try:
            note = int(note_str)
            if note < 0 or note > 10:
                print("Note invalide (doit être entre 0 et 10). La note ne sera pas enregistrée.")
                note = None
        except ValueError:
            print("Entrée invalide pour la note. La note ne sera pas enregistrée.")
            note = None
    commentaire = input("Entrez un commentaire (laissez vide pour aucun) : ").strip()
    livre_trouve["Commentaire"] = None if commentaire == "" else commentaire
    print(f"Le livre \"{livre_trouve['Titre']}\" est maintenant marqué comme lu.")

def afficher_par_statut(bibliotheque):
    print("\n*** Afficher les livres par statut (lus/non lus) ***")
    choix = input("Tapez '1' pour afficher les livres lus, '2' pour les livres non lus : ").strip()
    if choix not in ['1', '2']:
        print("Choix invalide. Opération annulée.")
        return
    if choix == '1':
        # Filtrer les livres lus
        livres_lus = [livre for livre in bibliotheque if livre["Lu"]]
        if not livres_lus:
            print("Aucun livre lu pour le moment.")
        else:
            print("Livres lus :")
            for livre in livres_lus:
                id_livre = livre["ID"]
                titre = livre["Titre"]
                auteur = livre["Auteur"]
                annee = livre["Année"]
                note = livre.get("Note", None)
                commentaire = livre.get("Commentaire", None)
                ligne = f"ID {id_livre} : \"{titre}\" par {auteur} ({annee}) - Lu : Oui"
                if note is not None:
                    ligne += f", Note : {note}/10"
                print(ligne)
                if commentaire:
                    print(f"    Commentaire : {commentaire}")
    else:  # choix == '2'
        livres_non_lus = [livre for livre in bibliotheque if not livre["Lu"]]
        if not livres_non_lus:
            print("Aucun livre non lu.")
        else:
            print("Livres non lus :")
            for livre in livres_non_lus:
                id_livre = livre["ID"]
                titre = livre["Titre"]
                auteur = livre["Auteur"]
                annee = livre["Année"]
                print(f"ID {id_livre} : \"{titre}\" par {auteur} ({annee}) - Lu : Non")

def trier_livres(bibliotheque):
    print("\n*** Trier les livres ***")
    print("Choisissez un critère de tri :")
    print("1. Année (croissant)")
    print("2. Auteur (alphabétique)")
    print("3. Note (décroissant)")
    choix = input("Votre choix (1/2/3) : ").strip()
    if choix not in ['1', '2', '3']:
        print("Choix invalide. Opération annulée.")
        return
    if choix == '1':
        livres_tries = sorted(bibliotheque, key=lambda x: x["Année"])
        print("Livres triés par année (du plus ancien au plus récent) :")
    elif choix == '2':
        livres_tries = sorted(bibliotheque, key=lambda x: x["Auteur"].lower())
        print("Livres triés par ordre alphabétique d'auteur :")
    else:
        livres_tries = sorted(bibliotheque, key=lambda x: -1 if x["Note"] is None else x["Note"], reverse=True)
        print("Livres triés par note (du meilleur au moins bon) :")
    for livre in livres_tries:
        id_livre = livre["ID"]
        titre = livre["Titre"]
        auteur = livre["Auteur"]
        annee = livre["Année"]
        lu = livre["Lu"]
        note = livre.get("Note", None)
        commentaire = livre.get("Commentaire", None)
        lu_str = "Oui" if lu else "Non"
        ligne = f"ID {id_livre} : \"{titre}\" par {auteur} ({annee}) - Lu : {lu_str}"
        if lu and note is not None:
            ligne += f", Note : {note}/10"
        print(ligne)
        if lu and commentaire:
            print(f"    Commentaire : {commentaire}")

def main():
    bibliotheque = charger_donnees("bibliotheque.json")
    print("=== Application Bibliothèque Personnelle ===")
    while True:
        print("\nMenu :")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer un livre comme lu")
        print("6. Afficher les livres lus/non lus")
        print("7. Trier les livres")
        print("8. Quitter")
        choix = input("Entrez votre choix : ").strip()
        if choix == '1':
            afficher_tous_les_livres(bibliotheque)
        elif choix == '2':
            ajouter_livre(bibliotheque)
        elif choix == '3':
            supprimer_livre(bibliotheque)
        elif choix == '4':
            rechercher_livre(bibliotheque)
        elif choix == '5':
            marquer_comme_lu(bibliotheque)
        elif choix == '6':
            afficher_par_statut(bibliotheque)
        elif choix == '7':
            trier_livres(bibliotheque)
        elif choix == '8':
            sauvegarder_donnees(bibliotheque, "bibliotheque.json")
            print("Données sauvegardées. Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")
            
if __name__ == "__main__":
    main()
