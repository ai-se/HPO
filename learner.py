from __future__ import division
from settings import *
from tuner import *
from scikitlearners2 import *
# __author__ = 'Wei'

class Learner(object):
  def __init__(i, train, tune, test):
    i.train = train
    i.tune = tune
    i.test = test

  def untuned(i):
    The.data.predict = i.test
    The.data.train = i.train
    i.default()
    The.option.tuning = False
    score = i.call()
    return score

  def tuned(i):
    The.data.predict = i.tune
    The.data.train = i.train
    The.option.tuning = True
    i.optimizer()
    The.option.tuning = False
    The.data.predict = i.test
    score = i.call()
    return score

  def call(i):
    raise NotImplementedError

  def optimizer(i):
    raise NotImplementedError

  def default(i):
    raise NotImplementedError


class Where(Learner):
  def __init__(i, train, tune, predict):
    super(Where, i).__init__(train, tune, predict)
    i.tunelst = ["The.tree.infoPrune",
                 "The.tree.min",
                 "The.option.threshold",
                 "The.where.wriggle",
                 "The.where.depthMax",
                 "The.where.depthMin",
                 "The.option.minSize",
                 "The.tree.prune",
                 "The.where.prune"]
    i.tune_min = [0.01, 1, 0.01, 0.01, 1, 1, 0.01, True, False]
    i.tune_max = [1, 10, 1, 1, 20, 6, 1, True, False]

  def default(i):
    The.option.baseLine = True
    The.tree.infoPrune = 0.33
    The.option.threshold = 0.5
    The.tree.min = 4
    The.option.minSize = 0.5  # min leaf size
    The.where.depthMin = 2  # no pruning till this depth
    The.where.depthMax = 10  # max tree depth
    The.where.wriggle = 0.2    #  set this at init()
    The.where.prune = False  # pruning enabled?
    The.tree.prune = True

  def call(i): return main()

  def optimizer(i):
    tuner = WhereDE(i)
    tuner.DE()


class CART(Learner):
  def __init__(i, train, tune, predict):
    super(CART, i).__init__(train, tune, predict)
    i.tunelst = ["The.cart.max_features",
                 "The.cart.max_depth",
                 "The.cart.min_samples_split",
                 "The.cart.min_samples_leaf",
                 "The.option.threshold"]
    i.tune_min = [0.01, 1, 2, 1, 0.01]
    i.tune_max = [1, 50, 20, 20, 1]

  def default(i):
    The.cart.max_features = None
    The.cart.max_depth = None
    The.cart.min_samples_split = 2
    The.cart.min_samples_leaf = 1
    The.option.threshold = 0.5

  def call(i):
    return cart()

  def optimizer(i):
    tuner = CartDE(i)
    tuner.DE()


class CART_clf(CART):
  def __init__(i, train, tune, predict):
    super(CART_clf, i).__init__(train, tune, predict)

  def call(i):
    return cartClassifier()


class RF(Learner):
  def __init__(i, train, tune, predict):
    super(RF, i).__init__(train, tune, predict)
    i.tunelst = ["The.rf.min_samples_split",
                 "The.rf.min_samples_leaf ",
                 "The.rf.max_leaf_nodes",
                 "The.rf.n_estimators",
                 "The.rf.max_features",
                 "The.option.threshold"]
    i.tune_min = [1, 2, 10, 50, 0.01, 0.01]
    i.tune_max = [20, 20, 50, 150, 1, 1]
    i.default_value = [2,1,None, 100,"auto",0.5]

  def default(i):
    # for key,val in zip(i.tunelst,i.default_value):
    #   setattr(key[],key[4:],val)
    # pdb.set_trace()
    The.option.threshold = 0.5
    The.rf.max_features = "auto"
    The.rf.min_samples_split = 2
    The.rf.min_samples_leaf = 1
    The.rf.max_leaf_nodes = None
    The.rf.n_estimators = 100

  def call(i): return rf()

class RF_clf(RF):
  def __init__(i,train,tune,predict):
    super(RF_clf, i).__init__(train,tune,predict)

  def call(i): return rfClassifier()


  def optimizer(i):
    tuner = RfDE(i)
    tuner.DE()