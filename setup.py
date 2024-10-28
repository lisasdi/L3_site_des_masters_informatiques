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

# importation des mots "stopwords" et les stocker dans une liste
def stopwords(input_file_english_txt = config['paths']['input_file_english_txt']):
    stopwordlist = []
    with open(input_file_english_txt) as fichier:
        for ligne in fichier:
            newstring = "".join([i for i in ligne if not i.isdigit()])
            newstring = re.sub("\n", "", newstring)
            stopwordlist.append(newstring)
    return stopwordlist


# fonction pour message_clean
def process(review):

    # radical
    stemmer = PorterStemmer()
    # HTML tags
    review = BeautifulSoup(review, "lxml").get_text()
    # urls
    url_regex = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
    review = re.sub(url_regex, "", review)
    # email adress
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    review = re.sub(email_pattern, "", review)
    # punctuation and numbers
    number_pattern = r"\d+"
    review = re.sub(number_pattern, " ", review)
    review = re.sub("[^a-zA-Z]", " ", review)
    # Cleaning white spaces
    review = re.sub(r"\s+", " ", review).strip()
    # converting into lowercase and splitting to eliminate stopwords
    review = review.lower()
    review = review.split()
    # review without stopwords
    swords = set(stopwords())  # conversion into set for fast searchin
    # rewiew = set(review) - swords
    review = [stemmer.stem(w) for w in review if w not in swords]
    # radical
    # splitted
    return " ".join(review)


# Fonction pour afficher la matrice de confusion
def plot_cm(y_test, y_pred, class_names,index_fold,chemin_results=config['paths']['chemin_results_composition']):
    disp = ConfusionMatrixDisplay(
        confusion_matrix=confusion_matrix(y_test, y_pred), display_labels=class_names
    )
    disp.plot(cmap=plt.cm.Blues)
    plt.suptitle(" composition " + str(index_fold))
    plt.savefig(chemin_results+ str(index_fold)+'.png')
    plt.close()



# afficher les comparaisons
def reporting(predictions, y_test, time, train_score, test_score,df_results):

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


def read(path,col1="label",col2="message",
         input_file_data_pkl=config['paths']['input_file_data_pkl'],
         chemin_results_Distribution=config['paths']['chemin_results_Distribution']):
    data = pd.read_csv(path, encoding="latin-1")
    # read file
    data.dropna(how="any", inplace=True, axis=1)  # how="any" : supprimer si valeur= NA
    # axis=1 : Drop columns which contain missing value // inplace= true : Whether to modify the DataFrame rather than creating a new one
    data.columns = [col1, col2]
    #print(data.head())
    # donner des valeurs numérique aux classes
    #data["label"] = data.label_num.map({0:"ham", 1:"spam"})
    data["label_num"] = data.label.map({"ham":0, "spam":1})
    # ajouter une colonne pour la taille du message, souvent les spams sont d'une grande taille
    data["message_len"] = data.message.apply(len)
    data["clean_msg"] = data.message.apply(process)
    #print(data.head())
    # save data
    with open(input_file_data_pkl, "wb") as f:
        pickle.dump(data, f)
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

