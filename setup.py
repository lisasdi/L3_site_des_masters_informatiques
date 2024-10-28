import requests
import pandas as pd

def get_coordinates_from_nominatim(address):
    """
    Utilise l'API Nominatim d'OpenStreetMap pour obtenir les coordonnées géographiques à partir d'une adresse.
    
    Arguments:
    - address: L'adresse à géocoder.
    
    Retourne:
    - Un dictionnaire contenant la latitude et la longitude.
    """
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data:
            location = data[0]
            return {'lat': location['lat'], 'lon': location['lon']}
        else:
            print("Adresse non trouvée")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur: {e}")
        return None

# Exemple de base de données locale simulée pour les codes INSEE et IRIS
insee_iris_db = {
    ('48.8566', '2.3522'): {'c_insee': '75056', 'c_iris': '0101'}
}

def get_insee_iris_from_coordinates(lat, lon):
    """
    Mappe les coordonnées géographiques aux codes INSEE et IRIS.
    
    Arguments:
    - lat: Latitude.
    - lon: Longitude.
    
    Retourne:
    - Un dictionnaire contenant les codes INSEE et IRIS.
    """
    # Simuler la recherche dans la base de données locale
    key = (str(round(float(lat), 4)), str(round(float(lon), 4)))
    return insee_iris_db.get(key, {'c_insee': 'UNKNOWN', 'c_iris': 'UNKNOWN'})

def EG_Insee_Iris(table_entree, top_TNP, civilite=None, prenom=None, nom=None, complement_nom=None, adresse=None, complement_adrs=None, lieu_dit=None, cp=None, ville=None, id_client=None, pays=None, email=None, tel=None):
    """
    Fonction de géocodage pour récupérer les codes INSEE et IRIS à partir d'une adresse.

    Arguments:
    - table_entree: Obligatoire, table de données, au format DataFrame.
    - top_TNP: Obligatoire, 1 si les champs civilite, nom et prénom sont dans le même champ, 0 si les champs sont dans des champs distincts.
    - civilite: Nom du champ contenant la civilité.
    - prenom: Nom du champ contenant le prénom.
    - nom: Nom du champ contenant le nom.
    - complement_nom: Nom du champ contenant le complément du nom.
    - adresse: Obligatoire, nom du champ contenant l’adresse.
    - complement_adrs: Nom du champ contenant le complément d’adresse.
    - lieu_dit: Nom du champ contenant le lieudit.
    - cp: Obligatoire, nom du champ contenant le code postal.
    - ville: Obligatoire, nom du champ contenant la ville.
    - id_client: Obligatoire, nom du champ contenant l’identifiant client.
    - pays: Nom du champ contenant le pays.
    - email: Nom du champ contenant l’adresse email.
    - tel: Nom du champ contenant le numéro de téléphone.

    Retourne:
    - Une table de données au format DataFrame contenant les champs initiaux ainsi que les champs supplémentaires: c_insee, c_iris, c_qualite_iris, codgeo.
    """
    # Ajouter les nouvelles colonnes avec des valeurs par défaut
    table_entree['c_insee'] = 'UNKNOWN'
    table_entree['c_iris'] = 'UNKNOWN'
    table_entree['c_qualite_iris'] = 8  # 8 : non trouvé ou non disponible
    table_entree['codgeo'] = 'UNKNOWN'
    
    for index, row in table_entree.iterrows():
        full_address = f"{row[adresse]}, {row[cp]} {row[ville]}, {row.get(pays, 'France')}"
        coordinates = get_coordinates_from_nominatim(full_address)
        
        if coordinates:
            lat = coordinates['lat']
            lon = coordinates['lon']
            insee_iris_codes = get_insee_iris_from_coordinates(lat, lon)
            
            table_entree.at[index, 'c_insee'] = insee_iris_codes['c_insee']
            table_entree.at[index, 'c_iris'] = insee_iris_codes['c_iris']
            table_entree.at[index, 'c_qualite_iris'] = 1  # 1 : correspondance exacte
            table_entree.at[index, 'codgeo'] = insee_iris_codes['c_insee'] + insee_iris_codes['c_iris']
    
    return table_entree

# Exemple d'utilisation
data = {
    'civilite': ['M.', 'Mme'],
    'prenom': ['Jean', 'Marie'],
    'nom': ['Dupont', 'Durand'],
    'adresse': ['123 Rue de Paris', '456 Avenue de la République'],
    'cp': ['75001', '75002'],
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
