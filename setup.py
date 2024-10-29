import pandas as pd
import numpy as np

# Exemple de chargement du fichier des prénoms avec sexe associé
# Remplacez 'fichier_prenom_sexe.csv' par le chemin réel de votre fichier
fichier_prenom_sexe = pd.read_csv('fichier_prenom_sexe.csv', usecols=["01_prenom", "02_genre"])

# Renommer les colonnes pour simplifier le mapping
fichier_prenom_sexe.columns = ["prenom", "genre"]

# Fonction enrichissement_age mise à jour avec fusion de la table des prénoms
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
        # Fusion des tables pour obtenir le sexe estimé
        tb_client = tb_client.merge(fichier_prenom_sexe, how='left', left_on=prenom, right_on="prenom")
        tb_client["e_sexe"] = tb_client["genre"].fillna("Inconnu")  # Si prénom absent dans le fichier, marquer comme "Inconnu"
    else:
        tb_client["e_sexe"] = tb_client[sexe]
    
    # Suppression de la colonne "genre" (pour éviter les doublons)
    tb_client.drop(columns=["genre"], inplace=True)
    
    # Estimation de l'année de naissance en utilisant `age_declare` si disponible
    tb_client["e_annee_naissance"] = np.where(
        tb_client[age_declare].notna(),
        2023 - tb_client[age_declare],
        2023 - np.random.randint(18, 80, tb_client.shape[0])
    )

    # Ajout d'autres champs simulés pour l'exemple
    tb_client["e_p_5ans"] = np.random.uniform(0.7, 0.95, tb_client.shape[0])
    tb_client["indice_conf_age"] = np.random.choice(["Confiance -", "Confiance +", "Confiance ++"], tb_client.shape[0])
    tb_client["e_top_age_ok"] = np.where(tb_client[age_declare].notna(), 1, 2)
    tb_client["e_age"] = 2023 - tb_client["e_annee_naissance"]

    # Ajustement de l'âge estimé si `ajust` est activé
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
