from curves import (
    distance,
    dynamic_distance,
    move_origin_to_zero,
    optimal_reparameterization,
)
from numpy import array, zeros, ones, linspace, sin, cos, exp
from numpy.random import random
from numpy.linalg import norm
from iisignature import sig
from signature import distance
from transformations import SRVT

N, d = 81, 2
I = linspace(0, 1, N)

a = zeros((N, d))
a[0:N, 0] = [4 * (1 - x) * x for x in I]
a[0:N, 1] = [20 * (x - 1) * (x - 0.5) * x for x in I]

b = zeros((N, d))
b[0:N, 0] = [sin(x) for x in 3.1415 * I]
b[0:N, 1] = [sin(x) for x in 2 * 3.1414 * I]

c = zeros((N, d))
c[0:N, 0] = [sin(x) for x in 2 * 3.1415 * I]
c[0:N, 1] = [sin(x) for x in 2 * 3.1415 * I]

d = zeros((N, d))
d[0:N, 0] = [20 * (x - 1) * (x - 0.5) * x for x in I]
d[0:N, 1] = [20 * (x - 1) * (x - 0.5) * x for x in I]


def f(u, v):
    return distance(u, v, 3)


def g(u, v):
    return dynamic_distance(u, v, 7)


dist = zeros(16)
dist[1] = f(a, b)
dist[2] = f(a, c)
dist[3] = f(a, d)

dist[4] = dist[1]  # (b,a)
dist[6] = f(b, c)  # (b,c)
dist[7] = f(b, d)  # (b,d)

dist[8] = dist[2]  # (c,a)
dist[9] = dist[6]  # (c,b)
dist[11] = f(c, d)  # (d,c)

dist[12] = dist[3]  # (d,a)
dist[13] = dist[7]  # (d,b)
dist[14] = dist[11]  # (d,c)


print("c(" + ", ".join(str(x) for x in dist) + ")")

import matplotlib.pyplot as plt

print("plot open.")
fig = plt.figure()
# ax.plot(a[:,0],a[:,1], 'b', label = "a")
# ax.plot(b[:,0],b[:,1], 'g', label = "b")
# ax.plot(c[:,0],c[:,1], 'y', label = "c")
# ax.plot(d[:,0],d[:,1], 'r', label = "d")

ax = fig.add_subplot(1, 2, 1)
ax.plot(a[:, 0], "b", label="a[x]")
ax.plot(a[:, 1], "bx", label="a[y]")
ax.plot(b[:, 0], "g", label="b[x]")
ax.plot(b[:, 1], "gx", label="b[y]")
plt.ylabel("y", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()

ax = fig.add_subplot(1, 2, 2)
ax.plot(c[:, 0], "y", label="c[x]")
ax.plot(c[:, 1], "yx", label="c[y]")
ax.plot(d[:, 0], "r", label="d[x]")
ax.plot(d[:, 1], "rx", label="d[y]")
plt.ylabel("y", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()


plt.show()
