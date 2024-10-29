import pandas as pd

# Supposons que table_enrichie est déjà enrichie avec les données socio-démographiques

# Exemple de table enrichie (pour illustration, à remplacer par votre table réelle)
table_enrichie = pd.DataFrame({
    "age": [30, 40, 35],
    "sexe": ["F", "M", "F"],
    "csp": ["Cadres", "Employés", "Artisans"],
    "e_dept": ["75", "75", "91"]  # Exemple de colonne de département
})

# 1. Comparaison d’une population cible vs population totale
test_profil_1 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil cible",
    table=table_enrichie,            # Table issue de l'enrichissement géomarketing
    var_age="age",                   # Champ contenant l'âge
    var_sexe="sexe",                 # Champ contenant le sexe, au format "F"/"M"
    var_pop1="csp",                  # Variable de restriction pour population cible
    modalite_pop1="Cadres"           # Modalité cible
)

# 2. Comparaison de 2 populations
test_profil_2 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil cible1 VS cible2",
    table=table_enrichie,
    var_age="age",
    var_sexe="sexe",
    var_pop1="csp",                 # Variable de la première population
    modalite_pop1="Cadres",         # Modalité pour la première population
    var_pop2="csp",                 # Variable de la deuxième population
    modalite_pop2="Employés"        # Modalité pour la deuxième population
)

# 3. Comparaison avec la population globale d’une zone géographique
test_profil_3 = EG_profil(
    sortie="chemin/vers/le/dossier/Sorties/Profil zone geo",
    table=table_enrichie,
    var_age="age",
    var_sexe="sexe",
    code_geo="e_dept",             # Code géographique, peut être "e_dept", "e_iris" ou "e_insee"
    zone_geo="75"                  # Valeur pour la zone géographique, par exemple "75" pour Paris
)

# Affichage des résultats (ou éventuellement vérifier les fichiers de sortie)
print("Profil cible vs population totale:", test_profil_1)
print("Comparaison de 2 populations:", test_profil_2)
print("Comparaison avec la population globale d’une zone géographique:", test_profil_3)
