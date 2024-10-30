import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, Reference

def generate_detailed_excel_report(df_summary, sortie_path, profil_type="Base Restos vs France"):
    """
    Génère un fichier Excel détaillé pour la comparaison d'une population cible avec des graphiques et une mise en page avancée.
    
    Args:
    - df_summary (pd.DataFrame): DataFrame contenant les statistiques de comparaison.
    - sortie_path (str): Chemin de sortie du fichier Excel.
    - profil_type (str): Titre du profil pour l'identification (par exemple "Base Restos vs France").
    """
    # Création du classeur Excel et ajout des feuilles
    wb = Workbook()
    ws_summary = wb.active
    ws_summary.title = "Profil Comparatif"

    # Titre du document
    ws_summary["A1"] = f"Profil - {profil_type} (1/2)"
    ws_summary["A1"].font = Font(size=14, bold=True)
    
    # Remplir la feuille avec les données de df_summary
    for row in dataframe_to_rows(df_summary, index=False, header=True):
        ws_summary.append(row)

    # Mise en forme conditionnelle et mise en page des colonnes
    for cell in ws_summary["C"]:
        if cell.value == df_summary.columns[1]:  # Nom de la première colonne de comparaison
            cell.fill = PatternFill(start_color="FFCCFF", end_color="FFCCFF", fill_type="solid")
        elif cell.value == df_summary.columns[2]:  # Nom de la deuxième colonne de comparaison
            cell.fill = PatternFill(start_color="CCFFCC", end_color="CCFFCC", fill_type="solid")
    
    # Création de graphiques pour chaque indicateur
    chart1 = BarChart()
    chart1.type = "col"
    chart1.title = "Comparaison des valeurs"
    data = Reference(ws_summary, min_col=2, max_col=3, min_row=2, max_row=len(df_summary)+1)
    cats = Reference(ws_summary, min_col=1, min_row=2, max_row=len(df_summary)+1)
    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)
    ws_summary.add_chart(chart1, "E5")
    
    # Sauvegarde du fichier Excel
    wb.save(sortie_path)

def EG_profil(sortie, table, var_age, var_sexe, var_comparaison1, var_comparaison2, var_pop1=None, modalite_pop1=None, code_geo=None, zone_geo=None):
    """
    Fonction pour réaliser des profils comparatifs sur des données enrichies et générer un fichier Excel détaillé.

    Args:
    - sortie (str): Chemin de sortie pour le fichier généré.
    - table (pd.DataFrame): Table de données à analyser.
    - var_age (str): Nom de la colonne contenant l'âge.
    - var_sexe (str): Nom de la colonne contenant le sexe.
    - var_comparaison1 (str): Nom de la première colonne à comparer.
    - var_comparaison2 (str): Nom de la deuxième colonne à comparer.
    - var_pop1 (str): Variable pour la population 1 (optionnel).
    - modalite_pop1 (str): Modalité pour la population 1 (optionnel).
    - code_geo (str): Code géographique pour la restriction (optionnel).
    - zone_geo (str): Zone géographique pour la restriction (optionnel).

    Returns:
    - pd.DataFrame: Un DataFrame avec les résultats des profils générés.
    """
    
    # Assurez-vous que le dossier de sortie existe
    os.makedirs(sortie, exist_ok=True)

    # Création des profils
    result_df = pd.DataFrame()  # Initialisation du DataFrame de résultat

    # Comparaison cible vs totale
    if var_pop1 and modalite_pop1:
        population_cible = table[table[var_pop1] == modalite_pop1]
        population_totale = table
        
        # Calcul des statistiques en utilisant les colonnes spécifiées pour comparaison
        result_cible_vs_totale = {
            'Indicateur': ["Age", "Sexe", "Situation Familiale", "PCS"],  # Noms des indicateurs
            var_comparaison1: [population_cible[var_age].mean(), population_cible[var_sexe].value_counts(normalize=True).get('F', 0) * 100,
                               50, 30],  # Données fictives pour exemple
            var_comparaison2: [population_totale[var_age].mean(), population_totale[var_sexe].value_counts(normalize=True).get('F', 0) * 100,
                               45, 28],  # Données fictives pour exemple
            'Indice': [120, 90, 110, 108]
        }
        
        result_df = pd.DataFrame(result_cible_vs_totale)

        # Enregistrement CSV et génération Excel détaillé
        csv_path = os.path.join(sortie, 'profil_cible_vs_totale.csv')
        result_df.to_csv(csv_path, index=False)
        excel_path = os.path.join(sortie, '2016_modele_profil_cible_détail.xlsx')
        generate_detailed_excel_report(result_df, excel_path)

    # Similar process for other types of comparisons

    return result_df

# Exemple d'utilisation de la fonction
table_enrichie = pd.DataFrame({
    "age": [30, 40, 35],
    "sexe": ["F", "M", "F"],
    "csp": ["Cadres", "Employés", "Artisans"],
    "e_dept": ["75", "75", "91"]  # Exemple de colonne de département
})

result1 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil cible",
    table=table_enrichie,
    var_age="age",
    var_sexe="sexe",
    var_comparaison1="csp",
    var_comparaison2="e_dept",
    var_pop1="csp",
    modalite_pop1="Cadres"
)

# Affichage des résultats
print("Profil cible vs population totale:", result1)
