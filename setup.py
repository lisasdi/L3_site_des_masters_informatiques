import numpy as np
import pandas as pd

# Exemple de DataFrame tb_client
tb_client = pd.DataFrame({
    "e_age": [30, 40, 25, 35, 50],  # Âges estimés
    "age_reel": [28, 42, 24, 36, 55],  # Âges réels
    "age_declare": [29, 39, 26, None, 52]  # Âges déclarés (None pour simuler un âge manquant)
})

# Vérification si l'âge estimé est aussi dans la plage de +/- 5 de l'âge déclaré
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

# Affichage du DataFrame pour voir les résultats
print(tb_client)
