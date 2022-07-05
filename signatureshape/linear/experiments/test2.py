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
from signature import sig_dist
from transformations import SRVT

N, d = 81, 1
I = linspace(0, 1, N)

a = zeros((N, d))
a[10:41, 0] = [1 - abs(x) for x in linspace(-1, 1, 31)]
a[40:71, 0] = [-1 + abs(x) for x in linspace(-1, 1, 31)]

b = zeros((N, d))
b[10:61, 0] = [1 - abs(x) for x in linspace(-1, 1, 51)]

c = zeros((N, d))
c[0:N, 0] = [sin(x) for x in linspace(0, 2 * 3.145, N)]

d = zeros((N, d))
d[10:20, 0] = [1 - abs(x) for x in linspace(-1, 0, 10)]
d[20:30, 0] = [1] * 10
d[30:40, 0] = [1 - abs(x) for x in linspace(0, 1, 10)]


def f(u, v):
    return sig_dist(u, v, 7)
    return dynamic_distance(u, v, 7)
    return sig_dist(SRVT(u, I), SRVT(v, I), 3)


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
ax = fig.add_subplot(2, 2, 1)
ax.plot(I, a[:, 0], "b", label="a")
plt.ylabel("f(x)", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 2, 2)
ax.plot(I, b[:, 0], "r", label="b")
plt.ylabel("f(x)", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 2, 3)
ax.plot(I, c[:, 0], "g", label="c")
plt.ylabel("f(x)", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 2, 4)
ax.plot(I, d[:, 0], "y", label="d")
plt.ylabel("f(x)", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()
plt.show()
