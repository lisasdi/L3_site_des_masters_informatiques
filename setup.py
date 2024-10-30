import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, Reference

def generate_excel_report(df_summary, sortie_path):
    """
    Génère un fichier Excel comparant une population cible avec une population totale.
    
    Args:
    - df_summary (pd.DataFrame): DataFrame contenant les statistiques de comparaison
    - sortie_path (str): Chemin de sortie du fichier Excel
    """

    # Création du classeur Excel et ajout de la feuille "Résumé"
    wb = Workbook()
    ws_summary = wb.active
    ws_summary.title = "Résumé"

    # Ajout des données de df_summary à la feuille "Résumé"
    for row in dataframe_to_rows(df_summary, index=False, header=True):
        ws_summary.append(row)

    # Mise en forme conditionnelle pour la colonne des différences
    for cell in ws_summary['D'][2:]:  # Exclut l'en-tête
        if isinstance(cell.value, (int, float)) and abs(cell.value) > 5:
            cell.fill = PatternFill(start_color="FF9999", end_color="FF9999", fill_type="solid")

    # Création d'un graphique de comparaison
    chart = BarChart()
    data = Reference(ws_summary, min_col=2, max_col=3, min_row=1, max_row=ws_summary.max_row)
    cats = Reference(ws_summary, min_col=1, min_row=2, max_row=ws_summary.max_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.title = "Comparaison Population Cible vs Totale"
    ws_summary.add_chart(chart, "F2")

    # Sauvegarde du fichier Excel
    wb.save(sortie_path)

def EG_profil(sortie, table, var_age, var_sexe, var_pop1=None, modalite_pop1=None, var_pop2=None, modalite_pop2=None, code_geo=None, zone_geo=None):
    """
    Fonction pour réaliser des profils comparatifs sur des données enrichies et générer un fichier Excel.

    Args:
    - sortie (str): Chemin de sortie pour le fichier généré.
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

    # Analyse et génération des profils
    result_df = pd.DataFrame()  # Initialisation du DataFrame de résultat

    if var_pop1 and modalite_pop1:  # Comparaison cible vs totale
        population_cible = table[table[var_pop1] == modalite_pop1]
        population_totale = table
        
        # Calcul des statistiques
        result_cible_vs_totale = {
            'Indicateur': ["Population cible", "Population totale"],
            'Effectif': [len(population_cible), len(population_totale)],
            'Pourcentage': [100 * len(population_cible) / len(population_totale), 100]
        }
        
        result_df = pd.DataFrame(result_cible_vs_totale)

        # Enregistrement CSV et génération Excel
        csv_path = os.path.join(sortie, 'profil_cible_vs_totale.csv')
        result_df.to_csv(csv_path, index=False)
        excel_path = os.path.join(sortie, '2016_modele_profil_cible.xlsx')
        generate_excel_report(result_df, excel_path)

    if var_pop1 and modalite_pop1 and var_pop2 and modalite_pop2:  # Comparaison de 2 populations
        population_cible1 = table[table[var_pop1] == modalite_pop1]
        population_cible2 = table[table[var_pop2] == modalite_pop2]
        
        result_cible1_vs_cible2 = {
            'Indicateur': ["Cible 1", "Cible 2"],
            'Effectif': [len(population_cible1), len(population_cible2)],
            'Pourcentage': [100 * len(population_cible1) / len(table), 100 * len(population_cible2) / len(table)]
        }
        
        result_df = pd.DataFrame(result_cible1_vs_cible2)

        # Enregistrement CSV et génération Excel
        csv_path = os.path.join(sortie, 'profil_cible1_vs_cible2.csv')
        result_df.to_csv(csv_path, index=False)
        excel_path = os.path.join(sortie, '2016_modele_profil_cible_vs_cible.xlsx')
        generate_excel_report(result_df, excel_path)

    if code_geo and zone_geo:  # Comparaison géographique
        population_geo = table[table[code_geo] == zone_geo]
        
        result_geo = {
            'Indicateur': ["Population géographique", "Population totale"],
            'Effectif': [len(population_geo), len(table)],
            'Pourcentage': [100 * len(population_geo) / len(table), 100]
        }
        
        result_df = pd.DataFrame(result_geo)

        # Enregistrement CSV et génération Excel
        csv_path = os.path.join(sortie, 'profil_zone_geo.csv')
        result_df.to_csv(csv_path, index=False)
        excel_path = os.path.join(sortie, '2016_modele_profil_zone_geo.xlsx')
        generate_excel_report(result_df, excel_path)

    return result_df
