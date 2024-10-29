import pandas as pd
import numpy as np

# Supposons que la fonction EG_age_sexe existe dans un package nommé INEnrichissement
# from INEnrichissement import EG_age_sexe 

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
    
    # Appel de la fonction fictive EG_age_sexe pour enrichir les données
    # La fonction EG_age_sexe devrait être importée depuis le package INEnrichissement et utilisée ici
    # Par exemple : 
    # result = EG_age_sexe(tb_client, prenom, sexe, age_declare, top_estim_sexe, codgeo, ajust, var_ajust)

    # Simulons des colonnes de résultats pour l'exemple
    tb_client["e_sexe"] = np.where(tb_client[prenom].str[-1].isin(["a", "e", "i"]), "F", "M") if top_estim_sexe == 1 else tb_client[sexe]
    tb_client["e_annee_naissance"] = 2023 - np.random.randint(18, 80, tb_client.shape[0])  # Ex. année naissance estimée entre 18 et 80 ans
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
# tb_client = pd.DataFrame({"prenom": ["Alice", "Bob", "Clara"], "codgeo": ["123450000", "234560000", "345670000"]})
# result = enrichissement_age(tb_client, prenom="prenom", sexe="NA", age_declare="NA", top_estim_sexe=1, codgeo="codgeo", ajust=1, var_ajust="sexe")
# print(result)
