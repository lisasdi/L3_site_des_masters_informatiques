import pandas as pd
import numpy as np
import configparser

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Traiter la colonne genre pour gérer les genres multiples
def choose_random_gender(gender_string):
    # Sépare les genres par la virgule et choisit un genre aléatoire
    genders = [g.strip().upper() for g in gender_string.split(',')]
    return np.random.choice(genders)
# Fonction enrichissement_age mise à jour avec fusion de la table des prénoms
def EG_age_sexe(tb_client, prenom, sexe="NA", age_declare="NA", top_estim_sexe=1, codgeo="codgeo", ajust=0, var_ajust="NA"):

    fichier_prenom_sexe = pd.read_csv(config['paths']['prenoms'],sep=';', usecols=["01_prenom", "02_genre"],encoding='latin1')

    # Renommer les colonnes pour simplifier le mapping
    fichier_prenom_sexe.columns = ["prenom", "genre"]
    fichier_prenom_sexe["prenom"]=fichier_prenom_sexe["prenom"].str.lower()




    # Appliquer la fonction pour choisir un genre
    fichier_prenom_sexe["genre"] = fichier_prenom_sexe["genre"].apply(choose_random_gender)
    tb_client["prenom"]=tb_client["prenom"].str.lower()
    # Estimation du sexe en fonction de top_estim_sexe
    if top_estim_sexe == 1:
        # Fusion des tables pour obtenir le sexe estimé
        tb_client = tb_client.merge(fichier_prenom_sexe, how='left', left_on=prenom, right_on="prenom")
        # Créer e_sexe en fonction de la présence de la colonne sexe
        if sexe=="NA"  or sexe not in tb_client.columns:
            tb_client["e_sexe"] = tb_client["genre"].fillna("Inconnu")  # Remplir avec le genre estimé
            
        else: 
            tb_client["e_sexe"] = np.where(tb_client[sexe].isna(),tb_client["genre"].fillna("Inconnu"),tb_client[sexe]) # Si prénom absent dans le fichier, marquer comme "Inconnu"
    
    # Suppression de la colonne "genre" (pour éviter les doublons)
    tb_client.drop(columns=["genre"], inplace=True)

    annee=int(config['paths']['annee'])

    # Estimation de l'année de naissance en utilisant `age_declare` si disponible
    if age_declare!="NA"  and age_declare in tb_client.columns:
        tb_client["e_annee_naissance"] = np.where(
            tb_client[age_declare].notna(),
            annee - tb_client[age_declare],
            annee - np.random.randint(1, 100, tb_client.shape[0])
        )
    else: 
        tb_client["e_annee_naissance"] = annee - np.random.randint(1, 100, tb_client.shape[0])
    # Ajout d'autres champs simulés pour l'exemple
    tb_client["e_age"] = annee - tb_client["e_annee_naissance"]
    # Ajustement de l'âge estimé si `ajust` est activé
    if ajust == 1:
        if var_ajust == "sexe" and sexe!="NA" :
            mean_age_by_sex = tb_client.groupby(sexe)["e_age"].transform("mean")
            tb_client["e_age"] = tb_client["e_age"] * 0.5 + mean_age_by_sex * 0.5
        else:
            mean_age = tb_client["e_age"].mean()
            tb_client["e_age"] = tb_client["e_age"] * 0.5 + mean_age * 0.5
    tb_client["e_age"] = tb_client["e_age"].round().astype(int)

    tb_client["age_reel"] =np.random.randint(0, 100, tb_client.shape[0])  # Simuler un âge réel entre 0 et 99 ans

    # Définir la plage pour l'âge déclaré s'il est disponible
    if age_declare!="NA"  and age_declare in tb_client.columns:
        tb_client["age_plage_min"] = np.where(
            age_declare!="NA",
            tb_client[age_declare].astype(float) - 5,
            tb_client["e_age"] - 5
        )
        tb_client["age_plage_max"] = np.where(
            age_declare !="NA",
            tb_client[age_declare].astype(float) + 5,
            tb_client["e_age"] + 5
        )
    else : 
        tb_client["age_plage_min"] =tb_client["e_age"] - 5
        tb_client["age_plage_max"] =tb_client["e_age"] + 5
    tb_client["difference"]=(tb_client["age_reel"]-tb_client["e_age"]).abs()

    # Vérifier si age_reel est dans la plage
    tb_client["e_p_5ans"] = np.where(
        (tb_client["age_reel"] >= tb_client["age_plage_min"]) & (tb_client["age_reel"] <= tb_client["age_plage_max"]),
        1.0- (tb_client["difference"]/5),  # Probabilité = 1 (dans la fourchette)
        0.0   # Probabilité = 0 (en dehors de la fourchette)
    )

    # Vérification si l'âge estimé est aussi dans la plage de +/- 5 de l'âge déclaré
    if age_declare!="NA"  and age_declare in tb_client.columns:
        tb_client["indice_conf_age"] = np.where(
            tb_client["age_declare"].notna(),  # Vérifie si age_declare est présent
            np.where(
            (tb_client["e_age"] >= tb_client["age_declare"] - 5) & (tb_client["e_age"] <= tb_client["age_declare"] + 5),
            "Confiance ++",  # Âge estimé dans l'intervalle de l'âge déclaré
            np.where(
            (tb_client["e_age"] >= tb_client["age_declare"] - 3) & (tb_client["e_age"] <= tb_client["age_declare"] + 3),
            "Confiance +",  # Âge estimé proche de l'âge déclaré
            "Confiance -"   # Âge estimé éloigné de l'âge déclaré
            )
            ),
            # Si age_declare n'est pas présent, on compare avec age_reel
            np.where(
                (tb_client["e_age"] >= tb_client["age_reel"] - 5) & (tb_client["e_age"] <= tb_client["age_reel"] + 5),
                "Confiance ++",  # Âge estimé dans l'intervalle de l'âge réel
                np.where(
                    (tb_client["e_age"] >= tb_client["age_reel"] - 3) & (tb_client["e_age"] <= tb_client["age_reel"] + 3),
                    "Confiance +",  # Âge estimé proche de l'âge réel
                    "Confiance -"   # Âge estimé éloigné de l'âge réel
                )
            )
        )
    else:
        tb_client["indice_conf_age"]=np.where(
                (tb_client["e_age"] >= tb_client["age_reel"] - 5) & (tb_client["e_age"] <= tb_client["age_reel"] + 5),
                "Confiance ++",  # Âge estimé dans l'intervalle de l'âge réel
                np.where(
                    (tb_client["e_age"] >= tb_client["age_reel"] - 3) & (tb_client["e_age"] <= tb_client["age_reel"] + 3),
                    "Confiance +",  # Âge estimé proche de l'âge réel
                    "Confiance -"   # Âge estimé éloigné de l'âge réel
                )
            )



    # Suppression de la colonne 
    tb_client.drop(columns=["age_plage_min"], inplace=True)
    tb_client.drop(columns=["difference"], inplace=True)
    tb_client.drop(columns=["age_plage_max"], inplace=True)
    tb_client.drop(columns=["age_reel"], inplace=True)


    #tb_client["e_top_age_ok"] = np.where(tb_client[age_declare].notna(), 1, 2)
    tb_client['e_top_age_ok'] = np.where((age_declare!="NA")&(age_declare in tb_client.columns),
                                            np.where(tb_client["age_declare"].notna(), 1,2),
                                            np.where(tb_client['e_age'].isna(), 3, 2))




    return tb_client

'''# Exemple d'utilisation
tb_client = pd.DataFrame({
    "prenom": ["adina", "Bob", "Clara", "David", "Julian", "Karine"],
    "codgeo": ["123450000", "234560000", "345670000", "456780000", "567890000", "678910000"],
    "age_declare": [25, None, 45, None, 32, None],
    "sexe": ["F", "M", "NA", "M", "M", "F"]
})

result = EG_age_sexe(
    tb_client=tb_client,
    prenom="prenom",
    sexe="NA",
    age_declare="age_declare",
    top_estim_sexe=1,       # Estimation du sexe à partir du prénom
    codgeo="codgeo",
    ajust=1,                # Ajustement de l'âge activé
    var_ajust="sexe"        # Ajustement basé sur la variable "sexe"
)

# Affichage du résultat
print(result)'''
