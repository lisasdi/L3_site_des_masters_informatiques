import pandas as pd

# Définir les noms des colonnes
columns = [
    'age_retraite', 'age_etud', 'RFMD911', 'TX_SEUL', 'TX_FAMMONO',
    'TX_COUPSENF', 'TX_COUPAENF', 'et_niv0', 'et_niv1', 'et_niv2',
    'propr', 'locat', 'locat_hlm', 'h_ind', 't_comm', 'typocom',
    'rev', 'c_indice_qualite_rev', 'codgeo', 't_mm', 't_m',
    't_p', 't_pp', 'c_indice_qualite_formation', 
    'c_indice_qualite_menage', 'c_indice_qualite_pcs', 
    'c_indice_qualite_logement'
]

# Créer un DataFrame vide avec les colonnes spécifiées
data = {col: [] for col in columns}
df = pd.DataFrame(data)

# Ligne de données à ajouter
new_row = [
    61.492561655, 20.368774861, 5286796.0, 0.2992502717, 0.0772720075,
    0.2878364175, 0.3356413033, 0.5949565723, 0.2942930658, 0.1107503619,
    0.5569637793, 0.4430362207, 0.1255349379, 0.6528859022, None, None,
    26088.555036, 0.0, '01', 0.3213259577, 0.2559894605, 0.2958020782,
    0.1268825036, 0.0, 1.0, 0.0, 0.0
]

# Ajouter la nouvelle ligne au DataFrame
df.loc[len(df)] = new_row

# Afficher le DataFrame avec la nouvelle ligne
print(df)

