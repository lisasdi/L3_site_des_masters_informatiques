import pandas as pd
import os

def EG_profil(sortie, table, var_age, var_sexe, var_pop1=None, modalite_pop1=None, var_pop2=None, modalite_pop2=None, code_geo=None, zone_geo=None):
    """
    Fonction pour réaliser des profils comparatifs sur des données enrichies.

    Args:
    - sortie (str): Chemin de sortie pour le fichier CSV généré.
    - table (pd.DataFrame): Table de données à analyser.
    - var_age (str): Nom de la colonne contenant l'âge.
    - var_sexe (str): Nom de la colonne contenant le sexe.
    - var_pop1 (str): Variable pour la population 1 (pour comparaisons spécifiques).
    - modalite_pop1 (str): Modalité pour la population 1.
    - var_pop2 (str): Variable pour la population 2 (pour comparaisons spécifiques).
    - modalite_pop2 (str): Modalité pour la population 2.
    - code_geo (str): Code géographique à utiliser pour une comparaison géographique.
    - zone_geo (str): Valeur géographique pour la restriction.

    Returns:
    - pd.DataFrame: Un DataFrame avec les résultats des profils générés.
    """
    
    # Assurez-vous que le dossier de sortie existe
    os.makedirs(sortie, exist_ok=True)

    # Exemple d'analyse (calculs de pourcentages, moyennes, etc.)
    if var_pop1 and modalite_pop1:  # Si la population 1 est spécifiée
        population_cible = table[table[var_pop1] == modalite_pop1]
        population_totale = table
        
        # Comparaison de la population cible avec la population totale
        result_cible_vs_totale = {
            'Total': len(population_totale),
            'Cible': len(population_cible),
            'Pourcentage Cible': (len(population_cible) / len(population_totale)) * 100
        }
        
        # Créez un DataFrame pour sauvegarder les résultats
        result_df = pd.DataFrame([result_cible_vs_totale])
        result_df.to_csv(os.path.join(sortie, 'profil_cible_vs_totale.csv'), index=False)

    if var_pop1 and modalite_pop1 and var_pop2 and modalite_pop2:  # Si les deux populations sont spécifiées
        population_cible1 = table[table[var_pop1] == modalite_pop1]
        population_cible2 = table[table[var_pop2] == modalite_pop2]
        
        # Comparaison entre les deux populations
        result_cible1_vs_cible2 = {
            'Cible 1': modalite_pop1,
            'Taille Cible 1': len(population_cible1),
            'Cible 2': modalite_pop2,
            'Taille Cible 2': len(population_cible2),
            'Pourcentage Cible 1': (len(population_cible1) / len(table)) * 100,
            'Pourcentage Cible 2': (len(population_cible2) / len(table)) * 100
        }
        
        # Créez un DataFrame pour sauvegarder les résultats
        result_df_2 = pd.DataFrame([result_cible1_vs_cible2])
        result_df_2.to_csv(os.path.join(sortie, 'profil_cible1_vs_cible2.csv'), index=False)

    if code_geo and zone_geo:  # Comparaison géographique
        population_geo = table[table[code_geo] == zone_geo]
        
        # Résumé géographique
        result_geo = {
            'Zone Géographique': zone_geo,
            'Taille Population': len(population_geo),
            'Pourcentage Population': (len(population_geo) / len(table)) * 100
        }
        
        # Créez un DataFrame pour sauvegarder les résultats
        result_df_geo = pd.DataFrame([result_geo])
        result_df_geo.to_csv(os.path.join(sortie, 'profil_zone_geo.csv'), index=False)

    return result_df if var_pop1 and modalite_pop1 else (result_df_2 if var_pop1 and modalite_pop1 and var_pop2 and modalite_pop2 else result_df_geo)

# Exemple d'utilisation de la fonction
# table_enrichie doit être définie dans votre contexte
# Assurez-vous que la table_enrichie est un DataFrame pandas
table_enrichie = pd.DataFrame({
    "age": [30, 40, 35],
    "sexe": ["F", "M", "F"],
    "csp": ["Cadres", "Employés", "Artisans"],
    "e_dept": ["75", "75", "91"]  # Exemple de colonne de département
})

# Appel des profils
result1 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil cible",
    table=table_enrichie,
    var_age="age",
    var_sexe="sexe",
    var_pop1="csp",
    modalite_pop1="Cadres"
)

result2 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil cible1 VS cible2",
    table=table_enrichie,
    var_age="age",
    var_sexe="sexe",
    var_pop1="csp",
    modalite_pop1="Cadres",
    var_pop2="csp",
    modalite_pop2="Employés"
)

result3 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil zone geo",
    table=table_enrichie,
    var_age="age",
    var_sexe="sexe",
    code_geo="e_dept",
    zone_geo="75"
)

# Affichage des résultats
print("Profil cible vs population totale:", result1)
print("Comparaison de 2 populations:", result2)
print("Comparaison avec la population globale d’une zone géographique:", result3)
