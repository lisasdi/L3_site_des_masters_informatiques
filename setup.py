# Rendre unique les prénoms par sélection d'un seul sexe
fichier_prenom_sexe = (
    fichier_prenom_sexe.groupby("prenom")
    .agg(lambda x: x.mode()[0] if not x.mode().empty else "Inconnu")  # Prendre le sexe le plus fréquent
    .reset_index()
)
