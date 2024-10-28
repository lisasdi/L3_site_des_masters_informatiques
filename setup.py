from preprocessing import plot_cm, reporting, read
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def cross_validation_modelfit(model_hyper, data, X, y, splits, df_results, pipeline_name):
    kf = KFold(n_splits=splits, random_state=1, shuffle=True)
    for fold, (train_index, test_index) in enumerate(kf.split(X), 1):
        X_train, X_test = np.array(X)[train_index], np.array(X)[test_index]
        y_train, y_test = y[train_index], y[test_index]
        df_results = training_model(model_hyper, data, X_train, X_test, y_train, y_test, df_results, pipeline_name, fold)
    return df_results

def tf_idf_function(X_train, input_file_vectorisation=config['paths']['input_file_vectorisation']):
    vect = CountVectorizer()
    X_train_dtm = vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit_transform(X_train_dtm)
    with open(input_file_vectorisation, "wb") as f:
        pickle.dump(vect, f)
    return X_train_dtm

def find_best_hyperparameters(model, params, X, y):
    X_train, _, y_train, _ = train_test_split(X, y, random_state=1)
    X_train_dtm = tf_idf_function(X_train)
    grid_search = GridSearchCV(model, param_grid=params, cv=5)
    grid_search.fit(X_train_dtm, y_train)
    return grid_search

def training_model(model_hyper, data, X_train, X_test, y_train, y_test, df_results, pipeline_name, fold=None):
    model = make_pipeline(CountVectorizer(), TfidfTransformer(), model_hyper)
    start = time.time()
    model.fit(X_train, y_train)
    elapsed_time = time.time() - start

    predictions = model.predict(X_test)
    plot_cm(y_test, predictions, data.label.unique(), f"{pipeline_name}_fold{fold}" if fold else pipeline_name)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    algo_name = f"{model_hyper.__class__.__name__}_{pipeline_name}"
    df_results = reporting({algo_name: predictions}, y_test, elapsed_time, train_score, test_score, df_results)
    
    model_path = config['paths']['input_file_model_training'] + f"_{pipeline_name}.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    return df_results

def run_pipelines(data, df_results):
    X1 = data.clean_msg_pipeline_1
    X2 = data.clean_msg_pipeline_2
    y = data.label_num

    # Hyperparamètres pour LogisticRegression et RandomForestClassifier
    param_grid_lr = {'C': [0.1, 1, 10, 100], 'penalty': ['l1', 'l2']}
    param_grid_rf = {'n_estimators': [200, 500], 'max_features': ['auto', 'sqrt'], 'max_depth': [4, 6, 8], 'criterion': ['gini', 'entropy']}

    # Tester les modèles sur les deux pipelines
    for X, pipeline_name in zip([X1, X2], ["pipeline_1", "pipeline_2"]):
        for model, params, model_name in [(LogisticRegression(), param_grid_lr, "RL"), (RandomForestClassifier(random_state=1), param_grid_rf, "RF")]:
            best_model = find_best_hyperparameters(model, params, X, y).best_estimator_
            print(f"Meilleur estimateur pour {model_name}_{pipeline_name} : ", best_model)
            df_results = using_train_test_split(best_model, data, X, y, df_results, f"{model_name}_{pipeline_name}")
    
    return df_results

def using_train_test_split(model_hyper, data, X, y, df_results, pipeline_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    df_results = training_model(model_hyper, data, X_train, X_test, y_train, y_test, df_results, pipeline_name)
    return df_results

# Préparer le dataframe de résultats
df_results = pd.DataFrame(columns=["Algorithm", "Precision", "Recall", "F1-Score", "Accuracy", "time", "train score", "test score"])

# Charger les données
input_file_data = config['paths']['input_file_data_csv']
input_file_data_pkl = config['paths']['input_file_data_pkl']
read(input_file_data)
with open(input_file_data_pkl, "rb") as f:
    datasms = pickle.load(f)

# Évaluer les modèles sur les deux pipelines de données
df_results = run_pipelines(datasms, df_results)

# Affichage des résultats
print(df_results)

# Statistiques
moyenne = df_results['Accuracy'].mean()
variance = df_results['Accuracy'].var()
std = df_results['Accuracy'].std()
print("Moyenne des scores : ", moyenne)
print("Écart-type des scores : ", std)
print("Variance des scores : ", variance)

# Graphe des scores avec la moyenne
plt.plot(np.arange(1, len(df_results.Accuracy) + 1), df_results.Accuracy, marker='o', linestyle='-')
plt.axhline(y=moyenne, linestyle='--', color='red')
plt.xlabel('Algo&Pipeline')
plt.ylabel('Accuracy')
plt.grid()
plt.savefig('../../result_plt/score.png')
