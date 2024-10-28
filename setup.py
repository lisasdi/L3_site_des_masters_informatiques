from sklearn.model_selection import train_test_split,GridSearchCV
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
from preprocessing import plot_cm, reporting, read
import time
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import KFold, cross_val_score
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import randint as sp_randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
# cross validation
''' modifier le code pour ajouter une fonction qui teste les deux données qui sont stocké respectivement dans data.clean_msg_pipeline_1 et dat.clean_msg_pipeline_2 
 mais au final df_result va contenir les deux resultats (dans df_result[algorithme] mettre = Regressionlogistique + nom du pipeline traité)
'''
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def cross_validation_modelfit(model_hyper,data, X, y, splits,df_results):
    
    kf = KFold(n_splits=splits, random_state=1, shuffle=True)
    #
    # préparation des listes pour stocker les résultats
    cv_scores = []
    cv_scores_std = []
    index_fold = 1
    for train_index, test_index in kf.split(X):
        X_train, X_test = np.array(X)[train_index], np.array(X)[test_index]
        y_train, y_test = y[train_index], y[test_index]
        df_results=training_model(model_hyper,data,X_train,X_test, y_train, y_test,index_fold,df_results)
        index_fold += 1
    return df_results
    
def tf_idf_function(X_train,input_file_vectorisation=config['paths']['input_file_vectorisation']):
    # instantiate the vectorizer
    vect = CountVectorizer()
    vect.fit(X_train)
    # combine fit and transform into a single step
    X_train_dtm = vect.fit_transform(X_train)
    # TF IDF
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit_transform(X_train_dtm)
    with open(input_file_vectorisation, "wb") as f:
        pickle.dump(vect, f)
    return X_train_dtm

def find_hyper_parameters(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    clf=DecisionTreeClassifier()
    clf1=LogisticRegression()
    X_train_dtm=tf_idf_function(X_train)
    '''    param_dist = {"max_depth": [None,3,10],
              "max_features":  [1,3,5,8,10],
              "min_samples_split": [2,5,10] ,#sp_randint(2, 11),
              "min_samples_leaf": [1,2,4], #sp_randint(1, 11),
              "criterion": ["gini", "entropy"]}'''
    param_grid = {
    'C': [0.1, 1, 10, 100],
    'penalty': ['l1', 'l2']
    }
    samples = 8  # number of random samples 
    GridSearch = GridSearchCV(clf1, param_grid=param_grid,cv=5)
    GridSearch.fit(X_train_dtm, y_train)
    return GridSearch

def training_model(model_hyper,data,X_train,X_test, y_train, y_test,index_fold,df_results,
                   input_file_model_training=config['paths']['input_file_model_training']):
    model = make_pipeline(
    CountVectorizer(),
    TfidfTransformer(),
    model_hyper)
    predictions = dict()
    start = time.time()
    model.fit(X_train, y_train)
    predictions["DT"+str(index_fold)] = model.predict(X_test)
    end = time.time() - start
    
    plot_cm(y_test, predictions["DT"+str(index_fold)], data.label.unique(),index_fold)

    # overfitting : underfitting
    train_score = model.score(X_train, y_train)
    test_score =model.score(X_test, y_test)
        # report
    df_results=reporting(predictions, y_test, end, train_score, test_score,df_results)
        # save the model
    with open(input_file_model_training +str(index_fold)+ ".pkl", "wb") as f:
        pickle.dump(model, f)
    return df_results

  
    
    
    
# train_test_split
def using_train_test_split(model_hyper,data, X, y,df_results):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
   

    index_fold=0
    df_results=training_model(model_hyper,data,X_train,X_test, y_train, y_test,index_fold,df_results)
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
input_file_data_pkl=config['paths']['input_file_data_pkl']


read(input_file_data)
# load the data
with open(input_file_data_pkl, "rb") as f:
    datasms = pickle.load(f)

#  define X and y (from the SMS data) for use with COUNTVECTORIZER
X = datasms.clean_msg_pipeline_2
y = datasms.label_num
print(X.shape)
print(y.shape)

randomCV=find_hyper_parameters(X,y)
model_hyper=randomCV.best_estimator_
print("best estim : ",randomCV.best_estimator_)
#appel fct train
df_results=using_train_test_split(model_hyper,datasms, X, y,df_results)

'''
cross validation
model_hyper=DecisionTreeClassifier(max_features=9, min_samples_split=5)
df_results=cross_validation_modelfit(model_hyper,datasms, X, y, 5,df_results)

'''
# reporting
print(df_results)
#moyenne score
moyenne=np.mean(df_results.Accuracy)
variance=np.var(df_results.Accuracy)
std=np.std(df_results.Accuracy)
print("moyenne des score",moyenne)
print("ecart type des score",std)
print("variance des score",variance)
#graphe des scores avec la moyenne 
folds=np.arange(1,len(df_results.Accuracy)+1)
plt.plot(folds,df_results.Accuracy,marker='o',linestyle='-')
plt.axhline(y=moyenne,linestyle='--',color='red')

plt.xlabel('Folds')
plt.ylabel('Accuracy')
plt.grid()

plt.savefig('../../result_plt/score.png')
