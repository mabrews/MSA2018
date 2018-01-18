import os
import lightgbm as lgb
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from scipy.stats import skew, boxcox
from sklearn.metrics import mean_absolute_error

os.chdir('C:/Users/mabre/Google Drive/Fall 3 Homework Team 10/Machine Learning Project')

#import dataset
data=pd.read_csv("allstate_train.csv", sep = ',', header = 0, index_col = 0)

#split into continuous, categorical, loss for preprocessing
data_cont = data.iloc[:,116:130]
data_cat = data.iloc[:,0:116] #use 115 if using TF-IDF for cat116
data_y = data.iloc[:,130]
data_y =  (1 + data.iloc[:,130])**0.25

#factorization on categorical
le = preprocessing.LabelEncoder()
for column in data_cat.columns:
    data_cat.loc[:,column] = le.fit_transform(data_cat[column])
    
# Compute skewness and do Box-Cox transformation
skewed_var = data_cont.apply(lambda x: skew(x.dropna()))
print("\nSkew in numeric variables:")
print(skewed_var)

# Transform features with skew > 0.25 (The threshold is set subjectively)
skewed_var = skewed_var[abs(skewed_var) > 0.25]
#skewed_var = skewed_var.drop(['cont10'])
skewed_var = skewed_var.index

data_cont = data_cont + 1
for i in skewed_var:
	data_cont[i], lam = boxcox(data_cont[i])

#concat cat and cont dataframes
data_preprocessed = pd.concat([data_cat,data_cont],axis = 1)

#split into train & test sets
X_train, X_test, y_train, y_test = train_test_split(data_preprocessed, data_y, test_size=0.3, train_size=0.7,
                                                    random_state=42)

#final training sets for allstate_test prediction
X_train = data_preprocessed.iloc[100:,]
X_test = data_preprocessed.iloc[0:100,]
y_train = data_y.iloc[100:,]
y_test = data_y.iloc[0:100,]

# create dataset for lightgbm
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# specify your configurations as a dict
params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'mae'}, #{'l2','mae'}
    'num_leaves': 50,
    'learning_rate': 0.01,
    'feature_fraction': 0.7, #0.9
    'bagging_fraction': 0.7, #0.8
    'bagging_freq': 5,
    'verbose': 0
    #'n_jobs': 4
}

print('Start training...')
# train
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=5000,
                valid_sets=lgb_eval,
                early_stopping_rounds=25)

print('Save model...')
# save model to file
gbm.save_model('model.txt')

print('Start predicting...')
# predict
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
# eval
y_pred_t = y_pred**4 - 1
y_test_t = y_test**4 - 1
print('The mae of prediction is:', mean_absolute_error(y_test_t, y_pred_t))

#75: 1142.295
#50: 1142ish
#31: 1144ish
#42: 1145.798
#50 with feature = bagging = 0.7: 1141.518
#50 with feature = bagging = 0.7 and LR = 0.005: 1142.176

y_pred_test = gbm.predict(data_preprocessed.iloc[0:100,])
print('The mae of prediction is:', mean_absolute_error(y_pred_test**4, data_y.iloc[0:100,]**4))

features = gbm.feature_importance()

# LightGBM, cross-validation
cv_result_lgb = lgb.cv(params, 
                       lgb_train, 
                       num_boost_round=5000, 
                       nfold=5, 
                       stratified=False, 
                       early_stopping_rounds=25, 
                       verbose_eval=100, 
                       show_stdv=True)

num_boost_rounds_lgb = len(cv_result_lgb['l1-mean'])
print('num_boost_rounds_lgb=' + str(num_boost_rounds_lgb))

# train model
model_lgb = lgb.train(params, 
                      lgb_train, 
                      num_boost_round=num_boost_rounds_lgb)

#eval
y_pred_cv = model_lgb.predict(X_train)
y_pred_cv_t = y_pred_cv**4 - 1
y_train_act = y_train**4 - 1
print('The mae of prediction is:', mean_absolute_error(y_pred_cv_t, y_train_act))

#1057??? - super overfit

y_pred_cv_test = model_lgb.predict(data_preprocessed.iloc[0:100,])
print('The mae of prediction is:', mean_absolute_error(y_pred_cv_test**4, data_y.iloc[0:100,]**4))

