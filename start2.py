# __author__ = 'WeiFu'
from __future__ import division
from settings import *
from os import listdir
from os.path import join, isfile
from sk import *
from smote import *
from os import getenv
from learner import *
import time
from sklearn.cross_validation import train_test_split
import pandas as pd


def createfile(objective):
  home_path = getenv("HOME")
  The.option.resultname = (home_path + '/Google Drive/EXP/myresult' + strftime(
    "%Y-%m-%d %H:%M:%S") + objective)
  f = open(The.option.resultname, 'w').close()


def writefile(s):
  global The
  f = open(The.option.resultname, 'a')
  f.write(s + '\n')
  f.close()


def genTuningData(path="./data_Wollongong/"):
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[:]:
    nextpath = join(path, folder)
    data_src = [join(nextpath, f) for f in listdir(nextpath) if isfile(
      join(nextpath, f)) and ".DS" not in f and "train_" in f]
    if len(data_src)>1:
      delTuningData()
    else:
      data_src = data_src[0]
    df = pd.read_csv(data_src, header=0)
    df = df.reindex(np.random.permutation(df.index))
    train, test = train_test_split(df, test_size=0.2)
    train.to_csv(data_src[:data_src.rindex("/") + 1] + "00training.csv",
                 index=False)
    test.to_csv(data_src[:data_src.rindex("/") + 1] + "00tuning.csv",
                index=False)


def delTuningData(path="./data_Wollongong/"):
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[:]:
    nextpath = join(path, folder)
    data_src = [join(nextpath, f) for f in listdir(nextpath) if
                isfile(join(nextpath, f)) and ".DS" not in f and "00" in f]
    os.remove(data_src[0])
    os.remove(data_src[1])


def start(obj, path="./data_Wollongong", isSMOTE=False):
  def keep(learner, score):  # keep stats from run
    NDef = learner + ": N-Del"
    YDef = learner + ": Y-Del"
    for j, s in enumerate(lst):
      # s[NDef] = s.get(NDef, []) + [(float(score[0][j] / 100))]
      s[YDef] = s.get(YDef, []) + [(float(score[1][j] / 100))]
      # [YDef] will void to use myrdiv.

  def printResult(dataname):
    def myrdiv(d):
      stat = []
      for key, val in d.iteritems():
        val.insert(0, key)
        stat.append(val)
      return stat

    print "\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20
    for j, k in enumerate(["pd", "pf", "prec", "f", "g", "w","auc"]):
      express = "\n" + "*" * 10 + " " + k + " " + "*" * 10
      writefile(express)
      print(express)
      rdivDemo(myrdiv(lst[j]))
    writefile("End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
    print "\n"

  global The
  The.option.tunedobjective = obj  # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0: "pd", 1: "pf", 2: "prec", 3: "f", 4: "g", 5: "combined",6:"auc"}
  createfile(objectives[The.option.tunedobjective])
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[:]:
    nextpath = join(path, folder)
    data = [join(nextpath, f) for f in listdir(nextpath) if
            isfile(join(nextpath, f)) and ".DS" not in f]
    # for i in range(len(data)):
    # pdb.set_trace()
    random.seed(1)
    pd, pf, prec, F, g, w, auc= {}, {}, {}, {}, {}, {}, {}
    lst = [pd, pf, prec, F, g, w, auc]
    expname = folder
    #   # try:
    #   #   predict = [data[i + 2]]
    #   #   tune = [data[i + 1]]
    #   #   if isSMOTE:
    #   #     train = ["./Smote" + data[i][1:]]
    #   #   else:
    #   #     train = [data[i]]
    #   # except IndexError, e:
    #     # break
    title = ("Tuning objective: " + objectives[
      The.option.tunedobjective] + "\nBegin time: " + strftime(
      "%Y-%m-%d %H:%M:%S"))
    writefile(title)
    writefile("Dataset: " + expname)
    for _ in xrange(5):
      for model in [CART_clf, RF_clf]:  # add learners here!
        for task in ["Tuned_", "Naive_"]:
          writefile("-" * 30 + "\n")
          timeout = time.time()
          name = task + model.__name__
          if task == "Tuned_":
            train = [data[0]]
            tune = [data[1]]
            predict = [data[2]]
          else:
            train = [data[3]]
            predict = [data[2]]
          thislearner = model(train, tune, predict)
          keep(name,
               thislearner.tuned() if task == "Tuned_" else
               thislearner.untuned())
          run_time = name + " Running Time: " + str(
            round(time.time() - timeout, 3))
          print run_time
          writefile(run_time)
      # delTuningData()
      # genTuningData()
    print folder + " done!"
    printResult(expname)


if __name__ == "__main__":
  for i in [6]:
    genTuningData()
    start(i)
