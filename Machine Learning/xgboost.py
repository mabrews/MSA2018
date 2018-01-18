import os
import csv
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
#import gensim
#import nltk
#import re
#import string
from collections import Counter
import math
import time
from sklearn.decomposition import PCA


os.chdir('C:/Users/mabre/Google Drive/Fall 3 Homework Team 10/Machine Learning Project')

#import csv
data=pd.read_csv("allstate_train.csv", sep = ',', header = 0, index_col = 0)

data_train = pd.read_csv("train.csv",sep = ',', header = 0, index_col = 0)
data_valid = pd.read_csv("valid.csv",sep = ',',header = 0, index_col = 0)
data = pd.concat([data_train,data_valid],axis = 0)
data = data.sort_index()

data_cat = data.iloc[:,72:116]
data_bin = data.iloc[:,0:72]

#replace columns with only values of A or B with 1 and 0, respectively
data_bin = data_bin.replace(to_replace = ['A','B'],value = [1, 0])

for column in data_bin.columns:
    data_bin[column]=data_bin[column].astype('bool')

#for column in data_bin.columns:
#    if len(data_bin[column].value_counts().tolist()) == 2:
#        for row in range(1, len(data_cat)):
#            if data_cat.loc[row,column] == 'A':
#                data_cat.loc[row,column] = 1
#            else: data_cat.loc[row,column] = 0
#        print(column)
    #test_cat.loc[:,column] = le.fit_transform(test_cat[column])
    #print(column)

#take a sample of the data for train/validate so my computer doesn't explode
#train, test = train_test_split(data, test_size=0.2, train_size=0.2,random_state=42)

#extract column for TF-IDF
cat116 = data.iloc[:,115].tolist()

counts = Counter(cat116)
print(counts)

for i in counts.keys():
    counts[i] = math.log((len(cat116)/counts[i]))
    #print(i)

cat116 = pd.DataFrame(cat116)
cat116 = cat116.replace(to_replace = counts.keys(),value = counts.values())
cat116.index += 1

tf_idf = pd.DataFrame()

#looping through all columns for TF-IDF

for column in data_cat.columns:
    term_list = data[column]
    counts = Counter(term_list)
    for i in counts.keys():
        counts[i] = math.log((188218/counts[i]))
    term_list = term_list.replace(to_replace = counts.keys(), value = counts.values())
    tf_idf = pd.concat([tf_idf,term_list],axis = 1)

data_columns = tf_idf.columns.tolist()
for i in range(len(data_columns)):
    data_columns[i] = data_columns[i]+'_TFIDF'

tf_idf.columns = data_columns

#PCA on TF-IDF
pca = PCA()
pca.fit(tf_idf)
loadings = pca.components_
loadings.shape
loadings

#tfidf = {}
#tfidf['A'] = math.log((counts['A']+counts['B'])/counts['A'])
#tfidf['B'] = math.log((counts['B'] + counts['A'])/counts['B'])
#
#for i in test:
#    d2[i] = Counter(d[i])
#    print(i)
#giving up on this approach for now - switch to one hot encoding
#
##trying one hot encoding - preprocessing
#test_cat = test.iloc[:,0:115]
#test_cont = test.iloc[:,116:130]
#test_y = test.iloc[:,130]
#le = preprocessing.LabelEncoder()
#for column in test_cat.columns:
#    test_cat.loc[:,column] = le.fit_transform(test_cat[column])
#    #print(column)
#
#enc = preprocessing.OneHotEncoder()
#preprocessing.OneHotEncoder(n_values = 'auto', categorical_features = test_cat,handle_unknown = 'error')
#test2 = enc.fit_transform(test_cat).toarray()
#test2 = pd.DataFrame(test2)
#
#test_cont = test_cont.reset_index(drop = True)
#test_y = test_y.reset_index(drop = True)
#test_preprocessed = pd.concat([test2,test_cont],axis = 1)
#
##repeat preprocessing process for training set
#train_cat = train.iloc[:,0:115]
#train_cont = train.iloc[:,116:130]
#train_y = train.iloc[:,130]
#le = preprocessing.LabelEncoder()
#for column in train_cat.columns:
#    train_cat.loc[:,column] = le.fit_transform(train_cat[column])
#    #print(column)
#
#enc = preprocessing.OneHotEncoder()
#preprocessing.OneHotEncoder(n_values = 'auto', categorical_features = train_cat,handle_unknown = 'error')
#train2 = enc.fit_transform(train_cat).toarray()
#train2 = pd.DataFrame(train2)
#
#train_cont = train_cont.reset_index(drop = True)
#train_y = train_y.reset_index(drop = True)
#train_preprocessed = pd.concat([train2,train_cont],axis = 1)

#need to rethink strategy - preprocess entire dataset before grabbing test/train sets
data_cont = data.iloc[:,116:130]
data_cont = pd.concat([data_cont,data.iloc[:,131]],axis = 1)
data_cat = data.iloc[:,0:116] #use 115 if using TF-IDF for cat116
data_y = data.iloc[:,130]
data_y =  (1 + data.iloc[:,130])**0.25

le = preprocessing.LabelEncoder()
for column in data_cat.columns:
    data_cat.loc[:,column] = le.fit_transform(data_cat[column])
    #print(column)

enc = preprocessing.OneHotEncoder()
preprocessing.OneHotEncoder(n_values = 'auto', categorical_features = data_cat,handle_unknown = 'error',dtype = 'bool')
data2 = enc.fit_transform(data_cat).toarray()

data_cat = pd.DataFrame(data2)
data_cat.index += 1

#reset indeces 
#data_cont = data_cont.reset_index(drop = True)
#data_y = data_y.reset_index(drop = True)

data_preprocessed = pd.concat([data_cat,tf_idf,data_cont],axis = 1)

data_columns = data_preprocessed.columns.tolist()
data_columns[813]='cat116'
data_preprocessed.columns = data_columns

del [data,data_cat,data_cont,data_bin,cat116]

#recreating test and train sets
X_train, X_test, y_train, y_test = train_test_split(data_preprocessed, data_y, test_size=0.3, train_size=0.7,
                                                    random_state=42)

#XGBOOST LETS GOOOOOOOOOO
# Specify sufficient boosting iterations to reach a minimum
num_round = 800

# Leave most parameters as default
param = {'silent':1, 'objective':'reg:gamma', 'booster':'gbtree', 'base_score':3}
param['nthread'] = 8
param['eval_metric'] = ['rmse','mae']

#other parameters I found on kaggle forums
params_xgb = {
            'seed': 0,
            'colsample_bytree': 0.7,
            'silent': 1,
            'subsample': 0.7,
            'objective': 'reg:linear',
            'max_depth': 12,
            'min_child_weight': 100,
            'booster': 'gbtree',
            'eval_metric': 'mae',
            'learning_rate': 0.1
            }


# Convert input data from numpy to XGBoost format
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

#cpu_res = {}
clf = xgb.train(params_xgb, dtrain, num_round, evals=[(dtest, 'test')], early_stopping_rounds = 15)

xgb_rounds = []
xgb_rounds.append(clf.best_iteration)
y_pred_xgb = clf.predict(dtest,ntree_limit=clf.best_ntree_limit)

y_pred_xgb = y_pred_xgb**4 - 1
y_test_t = y_test**4 - 1
print('The mae of prediction is:', mean_absolute_error(y_test_t, y_pred_t))

#current best test set mae = 1181.76
#1187.57 with one-hot encoding for all cat + clusters
#1184.52 with one-hot encoding for all cat, no clusters
#1186.97 with one-hot encoding for cat1 - cat115, TF_IDF for cat116, no clusters
#1184.91 with factorization for all cat, TF-IDF for some cats, no clusters