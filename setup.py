# Traiter la colonne genre pour gérer les genres multiples
def choose_random_gender(gender_string):
    # Sépare les genres par la virgule et choisit un genre aléatoire
    genders = [g.strip().upper() for g in gender_string.split(',')]
    return np.random.choice(genders)

# Appliquer la fonction pour choisir un genre
fichier_prenom_sexe["genre"] = fichier_prenom_sexe["genre"].apply(choose_random_gender)
