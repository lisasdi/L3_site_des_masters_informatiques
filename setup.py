# Import des fonctions d'enrichissement
from .geocodage import EG_Insee_Iris
from .enrichissement_age import EG_age_sexe
from .enrichissement_geomk import EG_Enrichissement_Geomk
from .profil import EG_profil
import pandas as pd
import os

def enrichissement_geographique(table_initiale, chemin_sortie):
    """
    Fonction principale d'enrichissement géomarketing qui applique les différentes étapes :
    1. Ajout de codes géographiques
    2. Enrichissement avec les données socio-démographiques
    3. Génération de profils pour analyse

    Args:
    - table_initiale (pd.DataFrame): Table de données d'origine.
    - chemin_sortie (str): Chemin vers le dossier de sortie pour les résultats.
    
    Returns:
    - pd.DataFrame: Table enrichie avec toutes les informations ajoutées.
    """
    
    # Étape 1: Ajout des codes géographiques via EG_Insee_Iris
    print("Étape 1: Ajout des codes géographiques")
    table_insee = EG_Insee_Iris(table_initiale)
    
    # Étape 2: Enrichissement socio-démographique avec l'âge et le sexe via EG_age_sexe
    print("Étape 2: Enrichissement par âge et sexe")
    table_age_sexe = EG_age_sexe(table_insee, "sexe", "age")
    
    # Étape 3: Enrichissement géomarketing avec les données socio-économiques
    print("Étape 3: Enrichissement géomarketing")
    table_enrichie = EG_Enrichissement_Geomk(table_age_sexe, "codgeo", "sexe", "age")
    
    # Vérification du dossier de sortie
    os.makedirs(chemin_sortie, exist_ok=True)
    
    # Étape 4: Génération de profils pour l'analyse
    print("Étape 4: Génération de profils")
    
    # Comparaison d’une population cible vs population totale
    EG_profil(
        sortie=os.path.join(chemin_sortie, "Profil cible"),
        table=table_enrichie,
        var_age="age",
        var_sexe="sexe",
        var_pop1="csp",
        modalite_pop1="Cadres"  # Exemple de modalité cible
    )
    
    # Comparaison de 2 populations
    EG_profil(
        sortie=os.path.join(chemin_sortie, "Profil cible1 VS cible2"),
        table=table_enrichie,
        var_age="age",
        var_sexe="sexe",
        var_pop1="csp",
        modalite_pop1="Cadres",
        var_pop2="csp",
        modalite_pop2="Employés"  # Exemple de deuxième modalité cible
    )
    
    # Comparaison avec la population globale d’une zone géographique
    EG_profil(
        sortie=os.path.join(chemin_sortie, "Profil zone geo"),
        table=table_enrichie,
        var_age="age",
        var_sexe="sexe",
        code_geo="e_dept",
        zone_geo="75"  # Exemple de département cible
    )
    
    # Sauvegarde de la table enrichie finale
    fichier_sortie = os.path.join(chemin_sortie, "table_enrichie_complete.csv")
    table_enrichie.to_csv(fichier_sortie, index=False)
    print(f"Table enrichie sauvegardée à: {fichier_sortie}")
    
    return table_enrichie

# Exemple d'utilisation
if __name__ == "__main__":
    # Chargement de la table initiale
    table_initiale = pd.DataFrame({
        "codgeo": ["75001", "75002", "75003"],
        "sexe": ["M", "F", "M"],
        "age": [30, 25, 40]
    })
    
    chemin_sortie = "chemin/vers/le/dossier/Sorties"
    
    # Appel de la fonction principale
    table_enrichie_finale = enrichissement_geographique(table_initiale, chemin_sortie)
