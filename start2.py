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


def createfile(objective):
  home_path = getenv("HOME")
  The.option.resultname = (home_path+'/Google Drive/EXP/myresult'
                           + strftime("%Y-%m-%d %H:%M:%S") + objective)
  f = open(The.option.resultname, 'w').close()


def writefile(s):
  global The
  f = open(The.option.resultname, 'a')
  f.write(s + '\n')
  f.close()


def start(obj,path="./data_Wollongong", isSMOTE= False):
  def keep(learner, score):  # keep stats from run
    NDef = learner + ": N-Def"
    YDef = learner + ": Y-Def"
    for j, s in enumerate(lst):
      s[NDef] = s.get(NDef, []) + [(float(score[0][j] / 100))]
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
    for j, k in enumerate(["pd", "pf", "prec", "f", "g","w"]):
      express = "\n" + "*" * 10 +" "+ k +" "+ "*" * 10
      writefile(express)
      print(express)
      rdivDemo(myrdiv(lst[j]))
    writefile("End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
    print "\n"

  global The
  The.option.tunedobjective = obj # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0: "pd", 1: "pf", 2: "prec", 3: "f", 4: "g", 5:"combined"}
  createfile(objectives[The.option.tunedobjective])
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[:]:
    nextpath = join(path, folder)
    data = [join(nextpath, f) for f in listdir(nextpath)
            if isfile(join(nextpath, f)) and ".DS" not in f]
    for i in range(len(data)):
      random.seed(1)
      pd, pf, prec, F, g, w= {}, {}, {}, {}, {},{}
      lst = [pd, pf, prec, F, g,w]
      expname = folder + "V" + str(i)
      try:
        predict = [data[i + 1]]
        tune = [data[i+1]]
        if isSMOTE:
          train = ["./Smote"+ data[i][1:]]
        else:
          train = [data[i]]
      except IndexError, e:
        print folder + " done!"
        break
      title =  ("Tuning objective: " +objectives[The.option.tunedobjective]
                + "\nBegin time: " + strftime("%Y-%m-%d %H:%M:%S"))
      # pdb.set_trace()
      writefile(title)
      writefile("Dataset: "+expname)
      for model in [RF_classifier]:  # add learners here!
        for task in ["Tuned_","Naive_"]:
          writefile("-"*30+"\n")
          timeout = time.time()
          name = task + model.__name__
          thislearner = model(train, tune, predict)
          keep(name, thislearner.tuned() if task == "Tuned_" else thislearner.untuned())
          run_time =name + " Running Time: " + str(round(time.time() - timeout, 3))
          print run_time
          writefile(run_time)
      printResult(expname)


if __name__ == "__main__":
  # SMOTE()
  for i in [2,3]:
    start(i)

