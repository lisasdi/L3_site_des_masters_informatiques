import pandas as pd
import numpy as np

# Exemple de dictionnaire associant des prénoms et leur sexe probable
prenom_sexe_dict = {
    "Alice": "F", "Marie": "F", "Sophie": "F", "Clara": "F",
    "Bob": "M", "David": "M", "Michel": "M", "Pierre": "M"
}

# Dictionnaire de probabilité basé sur les deux dernières lettres des prénoms
bigramme_sexe_dict = {
    "an": "M", "en": "M", "el": "M", "ic": "M",
    "ie": "F", "la": "F", "na": "F", "ra": "F"
}

# Fonction d'estimation du sexe en utilisant d'abord le dictionnaire, puis les bigrammes
def estimer_sexe(prenom):
    # Vérifie si le prénom est dans le dictionnaire de prénoms
    sexe_estime = prenom_sexe_dict.get(prenom)
    if sexe_estime is not None:
        return sexe_estime
    
    # Si le prénom n'est pas trouvé, utilise les deux dernières lettres (bigramme)
    bigramme = prenom[-2:].lower()
    return bigramme_sexe_dict.get(bigramme, "Inconnu")  # Renvoie "Inconnu" si pas de correspondance

# Fonction enrichissement_age mise à jour
def enrichissement_age(tb_client, prenom, sexe="NA", age_declare="NA", top_estim_sexe=1, codgeo="codgeo", ajust=0, var_ajust="NA"):
    """
    Fonction pour estimer l'âge des clients en fonction de leur prénom et lieu d'habitation.
    
    Args:
    - tb_client (pd.DataFrame) : table de données contenant les informations des clients.
    - prenom (str) : nom du champ contenant le prénom.
    - sexe (str) : nom du champ contenant le sexe ("F" ou "M"), par défaut "NA" si absent.
    - age_declare (str) : nom du champ contenant l'âge déclaré, par défaut "NA" si absent.
    - top_estim_sexe (int) : 1 pour estimer le sexe à partir du prénom, 0 sinon.
    - codgeo (str) : nom du champ contenant le code géographique.
    - ajust (int) : 1 pour ajuster l'âge, 0 sinon.
    - var_ajust (str) : nom de la variable pour l'ajustement, "NA" si pas d'ajustement.

    Returns:
    - pd.DataFrame : table enrichie avec des estimations d'âge et de sexe.
    """
    
    # Estimation du sexe en fonction de top_estim_sexe
    if top_estim_sexe == 1:
        tb_client["e_sexe"] = tb_client[prenom].apply(estimer_sexe)
    else:
        tb_client["e_sexe"] = tb_client[sexe]
    

    # Calcul de l'année de naissance en fonction de la colonne `age_declare` existante
    # Si `age_declare` est NaN (non renseigné), on garde la logique de génération aléatoire

    tb_client["e_annee_naissance"] = np.where(
    tb_client["age_declare"].notna(),  # Vérifie si `age_declare` est renseigné
    2023 - tb_client["age_declare"],    # Calcule l'année de naissance si l'âge est renseigné
    2023 - np.random.randint(18, 80, tb_client.shape[0])  # Sinon, génère un âge aléatoire
)

    tb_client["e_p_5ans"] = np.random.uniform(0.7, 0.95, tb_client.shape[0])  # Probabilité entre 0.7 et 0.95
    tb_client["indice_conf_age"] = np.random.choice(["Confiance -", "Confiance +", "Confiance ++"], tb_client.shape[0])
    tb_client["e_top_age_ok"] = np.where(tb_client[age_declare].notna(), 1, 2)
    tb_client["e_age"] = 2023 - tb_client["e_annee_naissance"]
    
    # Ajustement de l'âge estimé (si demandé)
    if ajust == 1:
        if var_ajust == "sexe" and sexe != "NA":
            mean_age_by_sex = tb_client.groupby(sexe)["e_age"].transform("mean")
            tb_client["e_age"] = tb_client["e_age"] * 0.5 + mean_age_by_sex * 0.5
        else:
            mean_age = tb_client["e_age"].mean()
            tb_client["e_age"] = tb_client["e_age"] * 0.5 + mean_age * 0.5

    return tb_client

# Exemple d'utilisation
tb_client = pd.DataFrame({
    "prenom": ["Alice", "Bob", "Clara", "David", "Julian", "Karine"],
    "codgeo": ["123450000", "234560000", "345670000", "456780000", "567890000", "678910000"],
    "age_declare": [25, None, 45, None, 32, None],
    "sexe": ["F", "M", "F", "M", "M", "F"]
})

result = enrichissement_age(
    tb_client=tb_client,
    prenom="prenom",
    sexe="sexe",
    age_declare="age_declare",
    top_estim_sexe=1,       # Estimation du sexe à partir du prénom
    codgeo="codgeo",
    ajust=1,                # Ajustement de l'âge activé
    var_ajust="sexe"        # Ajustement basé sur la variable "sexe"
)

# Affichage du résultat
print(result)
