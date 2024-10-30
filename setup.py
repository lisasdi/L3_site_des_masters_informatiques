import pandas as pd
import configparser

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Charger le fichier CSV contenant les codes postaux et les codes INSEE correspondants
def load_insee_data():
    return pd.read_csv(config['paths']['datainsee'], sep=';')  # Utiliser le séparateur ; pour le CSV

# Fonction pour obtenir le code INSEE à partir du code postal
def get_insee_from_postal_code(postal_code, insee_data):
    result = insee_data[insee_data['Code Postal'] == postal_code]
    if not result.empty:
        return result.iloc[0]['Code INSEE']
    else:
        return 'UNKNOWN'

def EG_Insee_Iris(table_entree, top_TNP, civilite=None, prenom=None, nom=None, complement_nom=None, adresse=None, complement_adrs=None, lieu_dit=None, cp=None, ville=None, id_client=None, pays=None, email=None, tel=None):

    # Charger les données INSEE depuis le fichier CSV
    insee_data=load_insee_data()
    # Ajouter les nouvelles colonnes avec des valeurs par défaut
    print(type(table_entree))
    table_entree['c_insee'] = 'UNKNOWN'
    table_entree['c_iris'] = 'UNKNOWN'
    table_entree['c_qualite_iris'] = 8  # 8 : non trouvé ou non disponible
    table_entree['codgeo'] = 'UNKNOWN'
    
    for index, row in table_entree.iterrows():
        postal_code = row[cp]
        insee_code = get_insee_from_postal_code(postal_code, insee_data)

        table_entree.at[index, 'c_insee'] = insee_code
        table_entree.at[index, 'c_iris'] = '0000'  
        table_entree.at[index, 'c_qualite_iris'] = 1  # 1 : correspondance exacte
        table_entree.at[index, 'codgeo'] = insee_code + '0000'
    
    return table_entree




'''# Exemple d'utilisation
data = {
    'civilite': ['M.', 'Mme'],
    'prenom': ['Jean', 'Marie'],
    'nom': ['Dupont', 'Durand'],
    'adresse': ['123 Rue de Paris', '145 rue de ménilmontant'],
    'cp': ['75001', '75020'],
    'ville': ['Paris', 'Paris'],
    'id_client': [1, 2],
    'pays': ['France', 'France'],
    'email': ['jean.dupont@example.com', 'marie.durand@example.com'],
    'tel': ['0102030405', '0607080910']
}
table_entree = pd.DataFrame(data)

# Appel de la fonction de géocodage
resultat_geocodage = EG_Insee_Iris(
    table_entree=table_entree,
    top_TNP=0,  # 0 signifie que civilite, nom et prénom sont dans des champs distincts
    civilite='civilite',
    prenom='prenom',
    nom='nom',
    adresse='adresse',
    cp='cp',
    ville='ville',
    id_client='id_client'
)

# Afficher le résultat
print(resultat_geocodage)
'''
