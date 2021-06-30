import numpy as np
import matplotlib.pyplot as plt

#%%
# 原点を通る直線による近似
def linerorigin(x,y):
  a=np.dot(x,y)/(x**2).sum()
  plt.scatter(x,y,color="k")
  xmax = x.max()
  plt.plot([0,xmax],[0,a*xmax],color="k")
  print(a)
  return plt.show()
#%%
# 一般直線による近似
def linercommon(x,y):
  n = len(x)
  a = ((np.dot(x,y) - y.sum() * x.sum() / n) /
  ((x ** 2).sum()-x.sum() ** 2 / n))
  b=(y.sum() - a * x.sum()) / n
  plt.scatter(x,y,color="k")
  xmax = x.max()
  plt.plot([0,xmax],[0,a*xmax],color="k")
  print(a)
  print(b)
  return plt.show()
