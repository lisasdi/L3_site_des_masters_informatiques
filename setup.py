# Import des fonctions d'enrichissement
from geocodage import EG_Insee_Iris
from enrichissement_age import EG_age_sexe
from enrechissemen_geomk import EG_Enrichissement_Geomk
from profil import EG_profil
import pandas as pd
import os

def enrichissement_geographique(table_initiale, chemin_sortie):
    
    # Étape 1: Ajout des codes géographiques via EG_Insee_Iris
    print("Étape 1: Ajout des codes géographiques")
    table_insee = EG_Insee_Iris(
        table_entree=table_initiale,
        top_TNP=0,  # 0 signifie que civilite, nom et prénom sont dans des champs distincts
        civilite='civilite',
        prenom='prenom',
        nom='nom',
        adresse='adresse',
        cp='cp',
        ville='ville',
        id_client='id_client')
    
    # Étape 2: Enrichissement socio-démographique avec l'âge et le sexe via EG_age_sexe
    print("Étape 2: Enrichissement par âge et sexe")
    table_age_sexe = EG_age_sexe(
            tb_client=table_insee,
            prenom="prenom",
            sexe="NA",
            age_declare="age_declare",
            top_estim_sexe=1,       # Estimation du sexe à partir du prénom
            codgeo="codgeo",
            ajust=1,                # Ajustement de l'âge activé
            var_ajust="sexe")
    
    # Étape 3: Enrichissement géomarketing avec les données socio-économiques
    print("Étape 3: Enrichissement géomarketing")
    table_enrichie = EG_Enrichissement_Geomk(table_age_sexe, "codgeo", "e_sexe", "age_declare")
    
    # Vérification du dossier de sortie
    os.makedirs(chemin_sortie, exist_ok=True)
    
    # Étape 4: Génération de profils pour l'analyse
    print("Étape 4: Génération de profils")
    
    # Comparaison d’une population cible vs population totale
    EG_profil(
        sortie=os.path.join(chemin_sortie, "Profil cible"),
        table=table_enrichie,
        var_age="e_age",
        var_sexe="e_sexe",
        var_pop1="ville",
        modalite_pop1="Paris"  # Exemple de modalité cible
    )
    
    # Comparaison de 2 populations
    EG_profil(
        sortie=os.path.join(chemin_sortie, "Profil cible1 VS cible2"),
        table=table_enrichie,
        var_age="e_age",
        var_sexe="e_sexe",
        var_pop1="i_rev",
        modalite_pop1="c_indice_qualite_logement",
        var_pop2="i_rev",
        modalite_pop2="c_indice_qualite_formation"  # Exemple de deuxième modalité cible
    )
    
    # Comparaison avec la population globale d’une zone géographique
    EG_profil(
        sortie=os.path.join(chemin_sortie, "Profil zone geo"),
        table=table_enrichie,
        var_age="e_age",
        var_sexe="e_sexe",
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
    'civilite': ['M.', 'Mme', 'M.', 'Mme', 'M.', 'Mme', 'M.', 'Mme'],
    'prenom': ['Jean', 'Marie', 'Paul', 'Sophie', 'Luc', 'Claire', 'Thomas', 'Émilie'],
    'nom': ['Dupont', 'Durand', 'Martin', 'Bernard', 'Leroy', 'Petit', 'Moreau', 'Giraud'],
    'adresse': [
        '123 Rue de Paris',
        '145 rue de ménilmontant',
        '200 Avenue des Champs',
        '300 Boulevard Saint-Germain',
        '456 Rue de Lyon',
        '789 Avenue de Marseille',
        '135 Boulevard de Toulouse',
        '246 Rue de Bordeaux'
    ],
    'cp': ['75001', '75020', '75008', '75005', '69001', '13001', '31000', '33000'],
    'ville': ['Paris', 'Paris', 'Paris', 'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Bordeaux'],
    'id_client': [1, 2, 3, 4, 5, 6, 7, 8],
    'pays': ['France', 'France', 'France', 'France', 'France', 'France', 'France', 'France'],
    "age_declare": [25, None, 30, 22, 40, 35, None, 28]
    })

    #table_initialeexec="Data/table_init.csv"
    chemin_sortie = "Sorties/Exemples"
    #table_enrichie_finale = enrichissement_geographique(table_initialeexec, chemin_sortie)
    
    # Appel de la fonction principale
    table_enrichie_finale = enrichissement_geographique(table_initiale, chemin_sortie)
