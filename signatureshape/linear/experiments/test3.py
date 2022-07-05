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

N, d = 80, 1
I = linspace(0, 1, N)

c = zeros((N, d))
c[0:N, 0] = [sin(x) for x in linspace(0, 2 * 3.145, N)]

A = []
for i in range(2, 20, 2):
    c = zeros((N, d))
    c[0:N, 0] = [sin(i * x) for x in linspace(0, 2 * 3.145, N)]
    A.append(norm(sig(c, 4)))

B = []
for i in range(80, 200, 10):
    c = zeros((i, d))
    c[0:i, 0] = [sin(x) for x in linspace(0, 2 * 3.145, i)]
    B.append(norm(sig(c, 4)))


import matplotlib.pyplot as plt

print("plot open.")
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(list(range(2, 20, 2)), A, "b", label="a")
plt.ylabel("sig(sin(Nx)), x=[0:80]", axes=ax)
plt.xlabel("N", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 1, 2)
ax.plot(list(range(80, 200, 10)), B, "r", label="b")
plt.ylabel("sig(x), x = [0:N]", axes=ax)
plt.xlabel("N", axes=ax)
ax.legend()
plt.show()
