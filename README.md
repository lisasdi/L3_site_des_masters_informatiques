import logging

# Configuration de la journalisation
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def traiter_fichiers(input_path, output_path):
    logging.info("Début du traitement des fichiers.")
    logging.debug(f"Fichier d'entrée : {input_path}, Fichier de sortie : {output_path}")
    
    try:
        # Simuler le traitement des fichiers
        logging.info("Traitement en cours...")
        # ... (ton code ici)
        logging.info("Traitement terminé avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors du traitement : {e}")

def afficher_chemins():
    logging.info("Affichage des chemins.")
    # Simuler l'affichage des chemins
    input_file = "/chemin/vers/ton/fichier/input.csv"
    output_file = "/chemin/vers/ton/fichier/output.csv"
    logging.debug(f"Chemin d'entrée : {input_file}")
    lo
