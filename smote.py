# __author__ = 'WeiFu'
from __future__ import division
from settings import *
from os import listdir
from os.path import join, isfile
from time import strftime
from table import *
import pdb
import os

def createfolder(new_src):
  if os.path.exists(new_src):
    return
  else:
    os.makedirs(new_src)  # generate new folders for each file

def norm(tbl, c, one):
  return (one.cells[c] - tbl.indep[c].lo) / (tbl.indep[c].hi - tbl.indep[c].lo + 0.00001)


def dist(tbl, i, j):
  deltas = 0
  num_indep = len(i.cells) - 1
  for c in range(num_indep):  # the last one is $<bug, vaoid that
    n1 = norm(tbl, c, i)
    n2 = norm(tbl, c, j)
    inc = (n1 - n2) ** 2
    deltas += inc
  return deltas ** 0.5 / (num_indep) ** 0.5


def nearest(tbl, y_def, one, k):
  out = []
  for i in y_def:
    temp = dist(tbl, i, one)
    if len(out) < k:
      out.append([temp, i])
    else:
      X = sorted(out, key=lambda x: x[0])
      for s, each in enumerate(X):
        if temp > each[0]:
          X[s] = [temp, i]
          break
      out = sorted(X, key=lambda x: x[0])
  return random.sample(out, 1)[0][-1]


def savetbl(t, rows, fname):

  def writetofile(f, lst):
    f.write(",".join(map(str,lst)) + '\n')
  createfolder(fname[:fname.rfind("/")])
  f = open(fname, 'wb')
  writetofile(f,[i.name for i in t.headers])  # write header
  for r in rows:
    writetofile(f, r.cells)
  f.close()

def _SMOTE1(tbl, k):
  non_def, y_def = [], []
  out_non_def, out_y_def = [], []
  for row in tbl._rows:
    if row.cells[-1] > 0:
      y_def.append(row)
    else:
      non_def.append(row)
  num_non_def = len(non_def)
  num_y_def = len(y_def)
  half = int((num_non_def + num_y_def) / 2)
  if num_y_def < num_non_def:
    out_non_def = random.sample(non_def, half)
  out_y_def = y_def
  num_to_smote = half - num_y_def
  # candidates = random.sample(y_def, num_to_smote)
  for _ in range(num_to_smote):
    one = random.sample(y_def,1)[0]
    neighbor = nearest(tbl, y_def, one, k)
    for col in range(len(neighbor.cells) - 1):  # -1 we need to get rid of $<bug
      diff = neighbor.cells[col] - one.cells[col]
      gap = random.uniform(0, 1)
      one.cells[col] = round(one.cells[col] + gap * diff,2)
    one.cells[-1]=int((one.cells[-1]+neighbor.cells[-1])/2)  # add the class label, here to make all mean
    out_y_def.append(one)
  out = out_y_def+out_non_def
  return out



def SMOTE(path="./data", k=5, ):
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[:]:
    nextpath = join(path, folder)
    data = [join(nextpath, f) for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for i in range(len(data)):
      tbl = table(data[i])
      newfilename ="./Smote"+ data[i][1:]
      out = _SMOTE1(tbl, k)
      savetbl(tbl,out,newfilename)




if __name__ == "__main__":
  SMOTE()
