# Lecture du fichier CSV pour informations régionales
    region_data = pd.read_csv(region_filepath)
    
    # Extraction du code INSEE depuis le code géographique (5 premiers caractères)
    enriched_data['Code INSEE'] = enriched_data[codgeo].str[:5]
    
    # Fusion des informations régionales à partir du Code INSEE
    enriched_data = enriched_data.merge(
        region_data,
        left_on='Code INSEE',
        right_on='Département',  # Assurez-vous que cette colonne est bien nommée "Département" dans le fichier
        how='left'
    )
    
    # Renommage des colonnes pour correspondre aux champs de sortie
    enriched_data.rename(columns={
        'Département': 'e_dept',     # Département de résidence
        'Région': 'e_Region',        # Région de résidence
        'Code Région': 'e_reg'       # Numéro de région de résidence
    }, inplace=True)
    
    return enriched_data
