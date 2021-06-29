import numpy as np
import matplotlib.pyplot as plt

# aの値を決定
def reg1dim1(x,y):
  a=np.dot(x,y)/(x**2).sum()
  return a

x = np.array([-7,2,3,5,7])
y = np.array([-5,3,-3,5,5])
a = reg1dim1(x,y)

plt.scatter(x,y,color="k")
xmax = x.max()
plt.plot([0,xmax],[0,a*xmax],color="k")
plt.show()
