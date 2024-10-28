import pandas as pd
from nltk.stem import PorterStemmer
import string
import re
from bs4 import BeautifulSoup
import pickle
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np
import seaborn as sns
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
input_file_english_txt = config['paths']['input_file_english_txt']

# Importation des mots "stopwords" et les stocker dans une liste
def stopwords(input_file_english_txt=config['paths']['input_file_english_txt']):
    stopwordlist = []
    with open(input_file_english_txt) as fichier:
        for ligne in fichier:
            newstring = "".join([i for i in ligne if not i.isdigit()])
            newstring = re.sub("\n", "", newstring)
            stopwordlist.append(newstring)
    return stopwordlist


# Fonction de nettoyage du message avec pipeline
def process(review, pipeline):
    stemmer = PorterStemmer()
    
    # Étape 1 : Suppression des balises HTML
    if pipeline.get("remove_html", True):
        review = BeautifulSoup(review, "lxml").get_text()
    
    # Étape 2 : Suppression des URLs
    if pipeline.get("remove_urls", True):
        url_regex = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
        review = re.sub(url_regex, "", review)
    
    # Étape 3 : Suppression des adresses email
    if pipeline.get("remove_emails", True):
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        review = re.sub(email_pattern, "", review)
    
    # Étape 4 : Suppression des chiffres
    if pipeline.get("remove_numbers", True):
        number_pattern = r"\d+"
        review = re.sub(number_pattern, " ", review)
    
    # Étape 5 : Suppression de la ponctuation et normalisation
    if pipeline.get("remove_punctuation", True):
        review = re.sub("[^a-zA-Z]", " ", review)
    
    # Étape 6 : Conversion en minuscules
    review = review.lower()
    
    # Étape 7 : Suppression des stopwords
    if pipeline.get("remove_stopwords", True):
        swords = set(stopwords())
        review = [word for word in review.split() if word not in swords]
    else:
        review = review.split()
    
    # Étape 8 : Application du stemming
    if pipeline.get("apply_stemming", True):
        review = [stemmer.stem(word) for word in review]
    
    # Retourner le texte nettoyé
    return " ".join(review)


# Fonction pour afficher la matrice de confusion
def plot_cm(y_test, y_pred, class_names, index_fold, chemin_results=config['paths']['chemin_results_composition']):
    disp = ConfusionMatrixDisplay(
        confusion_matrix=confusion_matrix(y_test, y_pred), display_labels=class_names
    )
    disp.plot(cmap=plt.cm.Blues)
    plt.suptitle("Composition " + str(index_fold))
    plt.savefig(chemin_results + str(index_fold) + '.png')
    plt.close()


# Affichage des comparaisons
def reporting(predictions, y_test, time, train_score, test_score, df_results):
    for name, y_pred in predictions.items():
        report = classification_report(y_test, y_pred, output_dict=True)
        df_results = pd.concat(
            [
                df_results,
                pd.DataFrame.from_dict(
                    {
                        "Algorithm": name,
                        "time": time,
                        "test score": test_score,
                        "train score": train_score,
                        "Accuracy": metrics.accuracy_score(y_test, y_pred),
                        "Precision": report["weighted avg"]["precision"],
                        "Recall": report["weighted avg"]["recall"],
                        "F1-Score": report["weighted avg"]["f1-score"],
                    },
                    orient="index",
                ).T,
            ],
            ignore_index=True,
        )
    return df_results


# Lecture et nettoyage des données avec différentes configurations de pipeline
def read(path, col1="label", col2="message",
         input_file_data_pkl=config['paths']['input_file_data_pkl'],
         chemin_results_Distribution=config['paths']['chemin_results_Distribution']):
    data = pd.read_csv(path, encoding="latin-1")
    data.dropna(how="any", inplace=True, axis=1)
    data.columns = [col1, col2]
    data["label_num"] = data.label.map({"ham": 0, "spam": 1})
    data["message_len"] = data.message.apply(len)
    
    # Définir deux pipelines différents pour le traitement
    pipeline_1 = {
        "remove_html": True,
        "remove_urls": True,
        "remove_emails": True,
        "remove_numbers": True,
        "remove_punctuation": True,
        "remove_stopwords": True,
        "apply_stemming": True
    }
    
    pipeline_2 = pipeline_1.copy()
    pipeline_2["remove_stopwords"] = False  # Ne pas supprimer les stopwords pour ce pipeline

    # Nettoyer les messages avec les deux pipelines et stocker les résultats
    data["clean_msg_pipeline_1"] = data.message.apply(lambda x: process(x, pipeline_1))
    data["clean_msg_pipeline_2"] = data.message.apply(lambda x: process(x, pipeline_2))

    # Sauvegarder les données nettoyées
    with open(input_file_data_pkl, "wb") as f:
        pickle.dump(data, f)
    
    # Visualiser la distribution des classes
    fig, ax = plt.subplots()
    data["label"].value_counts().plot.pie(
        explode=[0, 0.1],
        autopct="%1.1f%%",
        ax=ax,
        shadow=True,
        startangle=300,
        colors=["#b2b2b2", "#7575b2"],
    )
    ax.set_title("Distribution of spam and ham")
    ax.figure.savefig(chemin_results_Distribution)
    plt.close()
    return data
             
