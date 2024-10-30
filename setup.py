# setup.py
from setuptools import setup, find_packages

setup(
    name="INEnrichissement",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        # Les dépendances peuvent être spécifiées ici, si elles ne sont pas dans requirements.txt.
    ],
    include_package_data=True,  # Permet d'inclure des fichiers supplémentaires (comme ceux dans `data`)
    package_data={
        '': ['data/*'],  # Inclure tous les fichiers dans le dossier `data`
    },
    entry_points={
        'console_scripts': [
            'inenrichissement = INEnrichissement.main:main',  # Remplacez `main` par la fonction d'entrée
        ],
    },
    author="Votre Nom",
    description="Un package pour l'enrichissement de données géocodées, d'âge, et géomarketing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
