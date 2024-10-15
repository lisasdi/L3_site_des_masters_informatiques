import configparser

# Créer un objet configparser
config = configparser.ConfigParser()

# Lire le fichier de configuration
config.read('config.ini')

# Accéder aux chemins dans la section 'paths'
input_file = config['paths']['input_file']
output_file = config['paths']['output_file']

# Utilisation dans le code
print(f"Le fichier d'entrée se trouve à : {input_file}")
print(f"Le fichier de sortie se trouve à : {output_file}")

[paths]
input_file = /chemin/vers/ton/fichier/input.csv
output_file = /chemin/vers/ton/fichier/output.csv
