#This script requires training & validation sets from LightGBM
#or xgboost scripts

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import make_scorer, mean_absolute_error
from rgf.sklearn import RGFRegressor
import rgf_python

#RGF Model
rgf = RGFRegressor(max_leaf=4000,
                   algorithm="RGF_Sib",
                   test_interval=100,
                   loss="LS",
                   verbose=False)
n_folds = 3

#CV scoring
rgf_scores = cross_val_score(rgf,
                             X_train,
                             y_train,
                             scoring=make_scorer(mean_absolute_error),
                             cv=n_folds)


rgf_score = sum(rgf_scores)/n_folds
print('RGF Classfier MSE: {0:.5f}'.format(rgf_score))

y_pred_rgf = rgf.fit(X_train, y_train).predict(X_test)
y_pred_t_rgf = y_pred_rgf**4 - 1

print('The mae of prediction is:', mean_absolute_error(y_test_t, y_pred_t_rgf))

#MAE 1181 with max_leaf = 300
#MAE 1159 with max_leaf = 1000
#MAE 1148 with max_leaf = 2000
#MAE 1145 with max_leaf = 4000

y_pred_rgf_test = rgf.fit(X_train, y_train).predict(X_test)
print('The mae of prediction is:', mean_absolute_error(y_pred_rgf_test**4, data_y.iloc[0:100,]**4))
