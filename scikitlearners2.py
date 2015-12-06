from __future__ import division, print_function
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from main import *
from newabcd import sk_abcd
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score


def csv2py(f):
  if isinstance(f, list):
    tbl = [table(src) for src in f]  # tbl is a list of tables
    t = tbl[0]
    for i in range(1, len(tbl)):
      t._rows += tbl[i]._rows
    tbl = t
  else:
    tbl = table(f)
  return tbl


def _Abcd(predicted, actual):
  predicted_txt = []
   # abcd = Abcd(db='Traing', rx='Testing')
  global The

  def isDef(x):
    return "Defective" if x >= The.option.threshold else "Non-Defective"
    # use the.option.threshold for cart,
    # rf and where!!

  for data in predicted:
    # predicted_txt += [isDef(data)]  # this is for defect prediction, binary classes
    predicted_txt.append(data)  # for multiple classes, just use it
  score = sk_abcd(predicted_txt, actual)
  if The.option.tunedobjective == 6: # auc
    actual_binary = np.array([ 1 if i == "Delay" else 0 for i in actual ])
    predicted_binary = np.array([ 1 if i == "Delay" else 0 for i in predicted ])
    score[0].append(int(roc_auc_score(actual_binary,predicted_binary)*100))
    score[1].append(int(roc_auc_score(actual_binary,predicted_binary)*100))
  return score


# def learn(clf):
#   def conv(x):
#     return [float(i) for i in x]
#
#   testdata, actual = buildtestdata1(The.data.predict)
#   traintable = csv2py(The.data.train)
#   traindata_X = [conv(row.cells[:-1]) for row in traintable._rows]
#   traindata_Y = [(row.cells[-1]) for row in traintable._rows]
#   predictdata_X = [conv(row.cells[:-1]) for row in testdata]
#   predictdata_Y = [(row.cells[-1]) for row in testdata]
#   clf = clf.fit(traindata_X, traindata_Y)
#   array = clf.predict(predictdata_X)
#   predictresult = [i for i in array]
#   scores = _Abcd(predictresult, actual)
#   return scores

def learn(clf,class_col = 0):
  def cov(data):
    lst = [ "Delay" if i !="Nondelay" else i for i in data ]
    return lst
  def build(src):
    df = pd.read_csv(src,header = 0)
    train_Y =np.asarray(cov(df.ix[:,class_col].as_matrix()))
    df = df._get_numeric_data()
    train_X = df.as_matrix() # numpy array with numeric
    return train_X, train_Y

  train_X, train_Y = build(The.data.train[0])
  test_X,test_Y = build(The.data.predict[0])
  clf = clf.fit(train_X, train_Y)
  array = clf.predict(test_X)
  predictresult = [i for i in array]
  scores = _Abcd(predictresult, test_Y)
  return scores


def cart():
  clf = DecisionTreeRegressor(
    max_features=The.cart.max_features,
    max_depth=The.cart.max_depth,
    min_samples_split=The.cart.min_samples_split,
    min_samples_leaf=The.cart.min_samples_leaf,
    random_state=1)
  return learn(clf)


def cartClassifier():
  clf = DecisionTreeClassifier(
    max_features=The.cart.max_features,
    max_depth=The.cart.max_depth,
    min_samples_split=The.cart.min_samples_split,
    min_samples_leaf=The.cart.min_samples_leaf,
    random_state=1)
  return learn(clf)

def rf():
  clf = RandomForestRegressor(
    n_estimators=The.rf.n_estimators,
    max_features=The.rf.max_features,
    min_samples_split=The.rf.min_samples_split,
    min_samples_leaf=The.rf.min_samples_leaf,
    max_leaf_nodes=The.rf.max_leaf_nodes,
    random_state=1)
  return learn(clf)


def rfClassifier():
  clf = RandomForestClassifier(
    n_estimators=The.rf.n_estimators,
    max_features=The.rf.max_features,
    min_samples_split=The.rf.min_samples_split,
    min_samples_leaf=The.rf.min_samples_leaf,
    max_leaf_nodes=The.rf.max_leaf_nodes,
    random_state=1)
  # pdb.set_trace()
  return learn(clf)


def bayes():
  clf = GaussianNB()
  return learn(clf)


def logistic():
  clf = linear_model.LogisticRegression()
  return learn(clf)


if __name__ == "__main__":
  eval(cmd())
