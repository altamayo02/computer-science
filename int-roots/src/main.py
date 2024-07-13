import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import numpy as np

figure = plt.figure(figsize=(25/3, 125/16))
axes = plt.axes()

SCOPE = 1500
LINES = 150
X = np.arange(0, SCOPE, 100)
Y = np.arange(0, SCOPE, 100)

plt.xticks(X)
plt.yticks(Y)
#axes.xaxis.set_minor_locator(MultipleLocator(1))
#axes.yaxis.set_minor_locator(MultipleLocator(1))
axes.set_xlim(0, SCOPE)
axes.set_ylim(0, SCOPE)
axes.set_title('Roots')
axes.set_xlabel('X')
axes.set_ylabel('Y')

x = []
y = []
sumi = 0
for i in range(LINES):
	sumi += i
	x.append(sumi)
	y = list(x)
	y.reverse()
	axes.plot(x, y)
print(x)
print(y)

axes.plot([0, SCOPE], [0, SCOPE], label='sqrt(2)', c='purple')

axes.plot([0, SCOPE], [0, 2*SCOPE], label='sqrt(5)', c='teal')
axes.plot([0, 2*SCOPE], [0, SCOPE], c='teal')

axes.plot([0, 2*SCOPE], [0, 3*SCOPE], label='sqrt(13)', c='crimson')
axes.plot([0, 3*SCOPE], [0, 2*SCOPE], c='crimson')

plt.legend()
plt.grid()
plt.show()