   # Estimation du sexe en fonction de top_estim_sexe
    if top_estim_sexe == 1:
        # Fusion des tables pour obtenir le sexe estimé
        tb_client = tb_client.merge(fichier_prenom_sexe, how='left', left_on=prenom, right_on="prenom")
        
        # Créer e_sexe en fonction de la présence de la colonne sexe
        if sexe is None or sexe not in tb_client.columns:
            tb_client["e_sexe"] = tb_client["genre"].fillna("Inconnu")  # Remplir avec le genre estimé
        else:
            tb_client["e_sexe"] = np.where(tb_client[sexe].isna(), tb_client["genre"].fillna("Inconnu"), tb_client[sexe])

    # Suppression de la colonne "genre" (pour éviter les doublons)
    tb_client.drop(columns=["genre"], inplace=True)
