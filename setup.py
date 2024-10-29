tb_client["age_reel"] = 2023 - np.random.randint(0, 100, tb_client.shape[0])  # Simuler un âge réel entre 0 et 99 ans

    # Définir la plage pour l'âge déclaré s'il est disponible
    tb_client["age_plage_min"] = np.where(
        tb_client[age_declare] != "NA",
        tb_client[age_declare].astype(float) - 5,
        tb_client["e_age"] - 5
    )
    tb_client["age_plage_max"] = np.where(
        tb_client[age_declare] != "NA",
        tb_client[age_declare].astype(float) + 5,
        tb_client["e_age"] + 5
    )

    # Vérifier si age_reel est dans la plage
    tb_client["e_p_5ans"] = np.where(
        (tb_client["age_reel"] >= tb_client["age_plage_min"]) & (tb_client["age_reel"] <= tb_client["age_plage_max"]),
        1.0,  # Probabilité = 1 (dans la fourchette)
        0.0   # Probabilité = 0 (en dehors de la fourchette)
    )

    # On peut aussi estimer une probabilité réaliste (ex. : 70% de chance)
    tb_client["e_p_5ans"] = np.random.uniform(0.6, 1.0, tb_client.shape[0])  # Générer une probabilité aléatoire entre 0.6 et 1.0

    # Autres champs ajoutés
    tb_client["indice_conf_age"] = np.random.choice(["Confiance -", "Confiance +", "Confiance ++"], tb_client.shape[0])
    tb_client["e_top_age_ok"] = np.where(tb_client[age_declare] != "NA", 1, 2)

    # Ajustement de l'âge estimé si `ajust` est activé
    if ajust == 1:
        if var_ajust == "sexe" and sexe != "NA":
            mean_age_by_sex = tb_client.groupby(sexe)["e_age"].transform("mean")
            tb_client["e_age"] = tb_client["e_age"] * 0.5 + mean_age_by_sex * 0.5
        else:
            mean_age = tb_client["e_age"].mean()
            tb_client["e_age"] = tb_client["e_age"] * 0.5 + mean_age * 0.5

    return tb_client
