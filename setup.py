import pandas as pd

# Exemple de données pour tb_client
tb_client = pd.DataFrame({
    "sexe": ["F", "M", "F"],
    "age": [30, 40, 35]
})

# Lire les probabilités depuis le fichier CSV
sexe_age_proba = pd.read_csv("sexe_age.csv")

# Créer une colonne `sexe_age` dans tb_client pour la fusion
tb_client["sexe_age"] = tb_client["sexe"] + tb_client["age"].astype(str)

# Fusion des tables en utilisant la colonne `sexe_age` comme clé de correspondance
tb_client = tb_client.merge(sexe_age_proba, on="sexe_age", how="left")

# Renommer les colonnes du fichier source pour qu'elles correspondent à l'output souhaité
tb_client.rename(columns={
    "p_1enf": "e_proba_1_enfant",
    "p_2enf": "e_proba_2_enfants",
    "proba_m5": "e_proba_m5",
    "proba_5_10": "e_proba_5_10",
    "proba_10_15": "e_proba_10_15",
    "proba_15_20": "e_proba_15_20"
}, inplace=True)

# Suppression de la colonne temporaire `sexe_age` si elle n'est plus nécessaire
tb_client.drop(columns="sexe_age", inplace=True)

# Affichage du résultat
print(tb_client)
