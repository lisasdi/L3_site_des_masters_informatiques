import pandas as pd

def enrichissement_geomarketing(table_initiale, codgeo, var_sexe, var_age):
    """
    Enrichissement géomarketing des données socio-démographiques.
    
    Args:
    - table_initiale (pd.DataFrame): Table de données au format table
    - codgeo (str): Nom du champ contenant le code géographique
    - var_sexe (str): Nom du champ contenant le sexe
    - var_age (str): Nom du champ contenant l'âge
    
    Returns:
    - pd.DataFrame: Table enrichie avec des données socio-démographiques
    """
    
    # Vérification que les colonnes nécessaires existent dans la table_initiale
    required_columns = [codgeo, var_sexe, var_age]
    for col in required_columns:
        if col not in table_initiale.columns:
            raise ValueError(f"La colonne {col} est absente de la table_initiale.")
    
    # Simulation de l'enrichissement, car la fonction EG_Enrichissement_Geomk n'est pas définie
    enriched_data = table_initiale.copy()
    
    # Ajout de colonnes d'enrichissement (valeurs fictives pour l'exemple)
    enriched_data['e_PCS'] = "Catégorie X"  # Catégorie socio professionnelle estimée
    enriched_data['c_indice_qualite_pcs'] = 0.85  # Indice de qualité de l’estimation de la PCS
    enriched_data['e_situation_fam'] = "Célibataire"  # Situation familiale estimée
    enriched_data['c_indice_qualite_menage'] = 0.75  # Indice de qualité de l’estimation de la situation familiale
    enriched_data['e_etudes'] = "Licence"  # Niveau d’études estimé
    enriched_data['c_indice_qualite_formation'] = 0.80  # Indice de qualité de l’estimation du niveau d’études
    
    # Probabilités et classes estimées
    enriched_data['h_ind'] = 0.6  # Probabilité d’habiter en habitation individuelle
    enriched_data['locat_hlm'] = 0.3  # Probabilité d’habiter en HLM
    enriched_data['e_habitat_individuel'] = "Individuel"  # Classe d’habitation individuelle estimée
    enriched_data['e_habitat_hlm'] = "HLM"  # Classe d’habitation HLM estimée
    enriched_data['e_statut_hab'] = "Propriétaire"  # Statut d’habitation estimé
    enriched_data['c_indice_qualite_logement'] = 0.78  # Indice de qualité de l’estimation du statut d’habitation
    
    # Enfants estimés
    enriched_data['e_proba_1_enfant'] = 0.5  # Classe de probabilité d’avoir au moins 1 enfant
    enriched_data['e_proba_2_enfants'] = 0.3  # Classe de probabilité d’avoir au moins 2 enfants
    enriched_data['e_proba_m5'] = 0.2  # Classe de probabilité d’avoir 1 enfant de moins de 5 ans
    enriched_data['e_proba_5_10'] = 0.15  # Classe de probabilité d’avoir 1 enfant âgé entre 5 et 10 ans
    enriched_data['e_proba_10_15'] = 0.1  # Classe de probabilité d’avoir 1 enfant âgé entre 10 et 15 ans
    enriched_data['e_proba_15_20'] = 0.05  # Classe de probabilité d’avoir 1 enfant âgé entre 15 et 20 ans
    
    # Informations sur la commune
    enriched_data['e_typo_commune_2010'] = "Urbain"  # Typologie de la commune de résidence
    enriched_data['e_taille_commune'] = "Grande"  # Taille de la commune de résidence
    enriched_data['e_seg_commerces'] = "Commerce A"  # Segmentation commerce du lieu d’habitation
    enriched_data['e_sous_seg_commerces'] = "Sous-seg A"  # Sous segmentation commerce du lieu d’habitation
    enriched_data['e_seg_logement'] = "Logement A"  # Segmentation logement du lieu d’habitation
    
    # Revenu estimé
    enriched_data['i_rev'] = 35000  # Revenu annuel estimé
    enriched_data['e_revenus'] = "Moyen"  # Classe de revenu estimé
    enriched_data['e_decile'] = 5  # Décile de revenu estimé
    enriched_data['c_indice_qualite_rev'] = 0.82  # Indice de qualité de l’estimation du revenu
    
    # Informations géographiques
    enriched_data['e_dept'] = "75"  # Département de résidence
    enriched_data['e_region_9'] = "Île-de-France"  # Grande région de résidence
    enriched_data['e_Region'] = "Région X"  # Région de résidence
    enriched_data['e_lib_dept'] = "Paris"  # Libellé du département de résidence
    enriched_data['e_reg'] = "11"  # Numéro de région de résidence
    
    return enriched_data

# Exemple d'utilisation
table_initiale = pd.DataFrame({
    "codgeo": ["75001", "75002", "75003"],
    "var_sexe": ["M", "F", "M"],
    "var_age": [30, 25, 40]
})

testGeomk = enrichissement_geomarketing(table_initiale, "codgeo", "var_sexe", "var_age")

# Affichage du résultat
print(testGeomk)
