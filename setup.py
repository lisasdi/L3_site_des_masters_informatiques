# setup.py

from setuptools import setup, find_packages

setup(
    name="INEnrichissement",                    # Nom du package
    version="0.1",
    packages=find_packages(),                   # Recherche automatique des sous-packages
    install_requires=[                          # Liste des dépendances (dans requirements.txt)
        "pandas>=1.0", "geopy", "numpy"         # Exemple de dépendances, ajuste selon tes besoins
    ],
    author="Ton Nom",
    author_email="tonemail@example.com",
    description="Module d'enrichissement géomarketing",
    long_description=open("README.md").read(),  # Import du fichier README pour la description complète
    long_description_content_type="text/markdown",
    url="http://github.com/ton_github/INEnrichissement",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
