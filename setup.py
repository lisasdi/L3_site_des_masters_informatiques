import pandas as pd

def enrichissement_geomarketing(table_initiale, codgeo, var_sexe, var_age, proba_filepath):
    """
    Enrichissement géomarketing des données socio-démographiques avec ajout de probabilités d'avoir des enfants.
    
    Args:
    - table_initiale (pd.DataFrame): Table de données au format table
    - codgeo (str): Nom du champ contenant le code géographique
    - var_sexe (str): Nom du champ contenant le sexe
    - var_age (str): Nom du champ contenant l'âge
    - proba_filepath (str): Chemin du fichier CSV contenant les probabilités par sexe et âge.
    
    Returns:
    - pd.DataFrame: Table enrichie avec des données socio-démographiques
    """
    
    # Vérification que les colonnes nécessaires existent dans la table_initiale
    required_columns = [codgeo, var_sexe, var_age]
    for col in required_columns:
        if col not in table_initiale.columns:
            raise ValueError(f"La colonne {col} est absente de la table_initiale.")
    
    # Création d'une copie de la table pour enrichir les données
    enriched_data = table_initiale.copy()
    
    # Ajout des informations socio-démographiques simulées (exemple fictif)
    enriched_data['e_PCS'] = "Catégorie X"
    enriched_data['c_indice_qualite_pcs'] = 0.85
    enriched_data['e_situation_fam'] = "Célibataire"
    enriched_data['c_indice_qualite_menage'] = 0.75
    enriched_data['e_etudes'] = "Licence"
    enriched_data['c_indice_qualite_formation'] = 0.80
    
    # Lecture du fichier CSV contenant les probabilités d'enfants
    sexe_age_proba = pd.read_csv(proba_filepath)
    
    # Création de la colonne `sexe_age` dans `enriched_data` et `sexe_age_proba` pour la fusion
    enriched_data["sexe_age"] = enriched_data[var_sexe] + enriched_data[var_age].astype(str)
    sexe_age_proba["sexe_age"] = sexe_age_proba["sexe"] + sexe_age_proba["age"].astype(str)
    
    # Fusion des tables en utilisant `sexe_age` comme clé
    enriched_data = enriched_data.merge(sexe_age_proba, on="sexe_age", how="left")
    
    # Renommer les colonnes importées depuis le CSV pour qu'elles correspondent aux champs de sortie
    enriched_data.rename(columns={
        "p_1enf": "e_proba_1_enfant",
        "p_2enf": "e_proba_2_enfants",
        "proba_m5": "e_proba_m5",
        "proba_5_10": "e_proba_5_10",
        "proba_10_15": "e_proba_10_15",
        "proba_15_20": "e_proba_15_20"
    }, inplace=True)
    
    # Suppression de la colonne temporaire `sexe_age`
    enriched_data.drop(columns="sexe_age", inplace=True)
    
    # Informations géographiques et autres enrichissements fictifs pour compléter
    enriched_data['e_typo_commune_2010'] = "Urbain"
    enriched_data['e_taille_commune'] = "Grande"
    enriched_data['e_seg_commerces'] = "Commerce A"
    enriched_data['e_sous_seg_commerces'] = "Sous-seg A"
    enriched_data['e_seg_logement'] = "Logement A"
    
    enriched_data['i_rev'] = 35000
    enriched_data['e_revenus'] = "Moyen"
    enriched_data['e_decile'] = 5
    enriched_data['c_indice_qualite_rev'] = 0.82
    
    enriched_data['e_dept'] = "75"
    enriched_data['e_region_9'] = "Île-de-France"
    enriched_data['e_Region'] = "Région X"
    enriched_data['e_lib_dept'] = "Paris"
    enriched_data['e_reg'] = "11"
    
    return enriched_data

# Exemple d'utilisation
table_initiale = pd.DataFrame({
    "codgeo": ["75001", "75002", "75003"],
    "sexe": ["M", "F", "M"],
    "age": [30, 25, 40]
})

# Appel de la fonction en spécifiant le chemin du fichier CSV de probabilités
testGeomk = enrichissement_geomarketing(table_initiale, "codgeo", "sexe", "age", "sexe_age.csv")

# Affichage du résultat
print(testGeomk)
