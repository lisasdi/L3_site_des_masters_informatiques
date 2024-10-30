import pandas as pd
import configparser
from geocodage import load_insee_data

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')



def EG_Enrichissement_Geomk(table_initiale, codgeo, var_sexe, var_age):
    
    # Vérification que les colonnes nécessaires existent dans la table_initiale
    required_columns = [codgeo, var_sexe, var_age]
    for col in required_columns:
        if col not in table_initiale.columns:
            raise ValueError(f"La colonne {col} est absente de la table_initiale.")
    
    # Création d'une copie de la table pour enrichir les données
    enriched_data = table_initiale.copy()
    
    # Ajout des informations socio-démographiques simulées (exemple fictif)
    column_names = ['rev','t_comm','typocom','locat_hlm','c_indice_qualite_rev',
                    'c_indice_qualite_pcs','h_ind','c_indice_qualite_formation',
                    'c_indice_qualite_logement','c_indice_qualite_menage','codgeo']  
    maj = pd.read_csv(config['paths']['majdata'], sep=',', names=column_names,low_memory=False)

    # Fusion des informations régionales à partir du reg
    enriched_data = enriched_data.merge(
        maj,
        left_on='codgeo',
        right_on='codgeo',  
        how='left'
    )
    
    # Renommage des colonnes pour correspondre aux champs de sortie
    enriched_data.rename(columns={  
        'rev': 'i_rev',
        't_comm': 'e_taille_commune',
        'typocom': 'e_typo_commune_2010'         

    }, inplace=True)

    
    # Lecture du fichier CSV contenant les probabilités d'enfants
    sexe_age_proba = pd.read_csv(config['paths']['enfants'])


    # Création de la colonne `sexe_age` dans `enriched_data` et `sexe_age_proba` pour la fusion
    enriched_data["sexe_age"] = enriched_data[var_sexe] + enriched_data[var_age].astype(str)

    
    # Fusion des tables en utilisant `sexe_age` comme clé
    enriched_data = enriched_data.merge(sexe_age_proba, on="sexe_age", how="left")
    
    # Renommer les colonnes importées depuis le CSV pour qu'elles correspondent aux champs de sortie
    enriched_data.rename(columns={
        "p_1enf": "e_proba_1_enfant",
        "p_2enf": "e_proba_2_enfants",
        "p_m5": "e_proba_m5",
        "p_5_10": "e_proba_5_10",
        "p_10_15": "e_proba_10_15",
        "p_15_20": "e_proba_15_20"
    }, inplace=True)
    
    # Suppression de la colonne temporaire `sexe_age`
    enriched_data.drop(columns="sexe_age", inplace=True)
    
    # Informations géographiques et autres enrichissements fictifs pour compléter
    '''  
    enriched_data['e_seg_logement'] = "Logement A"
    enriched_data['e_revenus'] = "Moyen"
    enriched_data['e_decile'] = 5
    enriched_data['e_PCS'] = "Catégorie X"
    enriched_data['e_situation_fam'] = "Célibataire"
    enriched_data['e_etudes'] = "Licence

    '''
    # Lecture du fichier CSV pour informations régionales
    region_data=load_insee_data()
    region_data=region_data[['Code INSEE','Département','Région','Code Département','Code Région']]
    
    # Extraction du code INSEE depuis le code géographique (5 premiers caractères)
    enriched_data['Code INSEE'] = enriched_data[codgeo].str[:5]
    
    # Fusion des informations régionales à partir du Code INSEE
    enriched_data = enriched_data.merge(
        region_data,
        left_on='Code INSEE',
        right_on='Code INSEE',  # Assurez-vous que cette colonne est bien nommée "Département" dans le fichier
        how='left'
    )
    
    # Renommage des colonnes pour correspondre aux champs de sortie
    enriched_data.rename(columns={
        'Département': 'e_lib_dept',     # Département de résidence
        'Région': 'e_Region',        # Région de résidence
        'Code Région': 'e_reg' ,
        'Code Département': 'e_dept'      # Numéro de région de résidence
    }, inplace=True)
    enriched_data.drop(columns=["Code INSEE"], inplace=True)
    # Nettoyer la colonne pour retirer les crochets et les apostrophes
    enriched_data['e_Region'] = enriched_data['e_Region'].str.strip("[]").str.replace("'", "", regex=False)
    enriched_data['e_dept'] = enriched_data['e_dept'].str.strip("[]").str.replace("'", "", regex=False)
    enriched_data['e_lib_dept'] = enriched_data['e_lib_dept'].str.strip("[]").str.replace("'", "", regex=False)
    enriched_data['e_reg'] = enriched_data['e_reg'].fillna(0).astype(int)

    enriched_data['e_reg'] = enriched_data['e_reg'].round().astype(int)

    column_names = ['region_9','Dept']  # Remplacez par vos noms de colonnes
    reg9 = pd.read_csv(config['paths']['departements'], sep=',', names=column_names, header=None,on_bad_lines='skip')
    # Fusion des informations régionales à partir du reg
    enriched_data = enriched_data.merge(
        reg9,
        left_on='e_dept',
        right_on='Dept',  
        how='left'
    )
    
    # Renommage des colonnes pour correspondre aux champs de sortie
    enriched_data.rename(columns={  
        'region_9': 'e_region_9',        
    }, inplace=True)

    
    column_names = ['CODGEO','Seg1','sous_seg1']  # Remplacez par vos noms de colonnes
    commerces = pd.read_csv(config['paths']['commerces'], sep=',', names=column_names)
    # Fusion des informations régionales à partir du reg
    enriched_data = enriched_data.merge(
        commerces,
        left_on='codgeo',
        right_on='CODGEO',  
        how='left'
    )
    enriched_data.drop(columns="CODGEO", inplace=True)
    # Renommage des colonnes pour correspondre aux champs de sortie
    enriched_data.rename(columns={  
        'Seg1': 'e_seg_commerces', 
        'sous_seg1': 'e_sous_commerces'

    }, inplace=True)

    
    return enriched_data
'''
# Exemple d'utilisation
table_initiale = pd.DataFrame({
    "codgeo": ["64012", "75101", "010010000"],
    "sexe": ["M", "F", "M"],
    "age": [30, 25, 40]
})

# Appel de la fonction en spécifiant le chemin du fichier CSV de probabilités
testGeomk = EG_Enrichissement_Geomk(table_initiale, "codgeo", "sexe", "age")

# Affichage du résultat
print(testGeomk)'''
