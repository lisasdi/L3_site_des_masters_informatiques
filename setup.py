from preprocessing import plot_cm, reporting, read

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import randint as sp_randint
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def cross_validation_modelfit(model_hyper, data, X, y, splits, df_results, pipeline_name):
    kf = KFold(n_splits=splits, random_state=1, shuffle=True)
    cv_scores = []
    cv_scores_std = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = np.array(X)[train_index], np.array(X)[test_index]
        y_train, y_test = y[train_index], y[test_index]
        df_results = training_model(model_hyper, data, X_train, X_test, y_train, y_test, df_results, pipeline_name)
    return df_results

def tf_idf_function(X_train, input_file_vectorisation=config['paths']['input_file_vectorisation']):
    vect = CountVectorizer()
    vect.fit(X_train)
    X_train_dtm = vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit_transform(X_train_dtm)
    with open(input_file_vectorisation, "wb") as f:
        pickle.dump(vect, f)
    return X_train_dtm

def find_hyper_parameters(model,params,X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    X_train_dtm = tf_idf_function(X_train)

    GridSearch = GridSearchCV(model, param_grid=params, cv=5)
    GridSearch.fit(X_train_dtm, y_train)
    return GridSearch

def training_model(model_hyper, data, X_train, X_test, y_train, y_test, df_results, pipeline_name,
                   input_file_model_training=config['paths']['input_file_model_training']):
    model = make_pipeline(
        CountVectorizer(),
        TfidfTransformer(),
        model_hyper
    )
    predictions = dict()
    start = time.time()
    model.fit(X_train, y_train)
    predictions[f"{pipeline_name}"] = model.predict(X_test)
    end = time.time() - start

    plot_cm(y_test, predictions[f"{pipeline_name}"], data.label.unique(), pipeline_name)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    # Nom de l'algorithme avec le pipeline
    algo_name = f"{model_hyper.__class__.__name__}_{pipeline_name}"
    df_results = reporting({algo_name: predictions[f"{pipeline_name}"]}, y_test, end, train_score, test_score, df_results)

    with open(input_file_model_training + f"_{pipeline_name}.pkl", "wb") as f:
        pickle.dump(model, f)
    return df_results

def using_train_test_split(model_hyper, data, X, y, df_results, pipeline_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    df_results = training_model(model_hyper, data, X_train, X_test, y_train, y_test, df_results, pipeline_name)
    return df_results

def test_pipelines(data, df_results):
    # Test avec clean_msg_pipeline_1
    X1 = data.clean_msg_pipeline_1
    y = data.label_num
    # Trouver les meilleurs hyperparamètres
    clf = LogisticRegression()
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'penalty': ['l1', 'l2']
    }
    randomCV = find_hyper_parameters(clf,param_grid,X1, y)
    model_hyper = randomCV.best_estimator_
    print("Meilleur estimateur : ", model_hyper)
    df_results = using_train_test_split(model_hyper, data, X1, y, df_results, "pipeline_1")
    
    # Test avec clean_msg_pipeline_2
    X2 = data.clean_msg_pipeline_2
    randomCV = find_hyper_parameters(clf,param_grid,X2, y)
    model_hyper = randomCV.best_estimator_
    print("Meilleur estimateur : ", model_hyper)
    df_results = using_train_test_split(model_hyper, data, X2, y, df_results, "pipeline_2")
    
    return df_results

df_results = pd.DataFrame(
    columns=[
        "Algorithm",
        "Precision",
        "Recall",
        "F1-Score",
        "Accuracy",
        "time",
        "train score",
        "test score",
    ]
)

input_file_data = config['paths']['input_file_data_csv']
input_file_data_pkl = config['paths']['input_file_data_pkl']

read(input_file_data)
with open(input_file_data_pkl, "rb") as f:
    datasms = pickle.load(f)


# Appel de la fonction test_pipelines pour évaluer les deux versions des données
df_results = test_pipelines(datasms, df_results)

# Affichage des résultats
print(df_results)

# Calcul des statistiques
moyenne = np.mean(df_results.Accuracy)
variance = np.var(df_results.Accuracy)
std = np.std(df_results.Accuracy)
print("Moyenne des scores : ", moyenne)
print("Écart-type des scores : ", std)
print("Variance des scores : ", variance)

# Graphe des scores avec la moyenne
folds = np.arange(1, len(df_results.Accuracy) + 1)
plt.plot(folds, df_results.Accuracy, marker='o', linestyle='-')
plt.axhline(y=moyenne, linestyle='--', color='red')
plt.xlabel('Algo&pipeline')
plt.ylabel('Accuracy')
plt.grid()
plt.savefig('../../result_plt/score.png')
 
