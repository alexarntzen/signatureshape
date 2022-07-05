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
a[0:N, 0] = [20 * (x - 1) * (x - 0.5) * x for x in linspace(0, 1, N)]

b = zeros((N, d))
b[0:N, 0] = [sin(x) for x in linspace(0, 3.145, N)]

c = zeros((N, d))
c[0:N, 0] = [sin(x) for x in linspace(0, 2 * 3.145, N)]

d = zeros((N, d))
d[0:N, 0] = [4 * (1 - x) * x for x in linspace(0, 1, N)]

sup = zeros((N, 4))
sup[0:N, 0] = a[:, 0]
sup[0:N, 1] = b[:, 0]
sup[0:N, 2] = c[:, 0]
sup[0:N, 3] = d[:, 0]

a_sig = sig(a, 5)
b_sig = sig(b, 5)
c_sig = sig(c, 5)
d_sig = sig(d, 5)
sup_sig = sig(sup, 2)

import matplotlib.pyplot as plt

print("plot open.")
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(I, a[:, 0], "b", label="a: 20*x*(x-0.5)*(x-1)")
ax.plot(I, b[:, 0], "r", label="b: sin(pi*x)")
ax.plot(I, c[:, 0], "g", label="c: sin(2*pi*x)")
ax.plot(I, d[:, 0], "y", label="d: 4*(1-x)*x")
plt.ylabel("f(x)", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 1, 2)
ax.plot(a_sig, "b", label="a: 20*x*(x-0.5)*(x-1)")
ax.plot(b_sig, "r", label="b: sin(pi*x)")
ax.plot(c_sig, "g", label="c: sin(2*pi*x)")
ax.plot(sup_sig, "y", label="d: 4*(1-x)*x")
plt.ylabel("f(x)", axes=ax)
plt.xlabel("x", axes=ax)
ax.legend()


plt.show()
