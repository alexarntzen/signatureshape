from .curves import (
    distance,
    dynamic_distance,
    move_origin_to_zero,
    optimal_reparameterization,
)
from numpy import array, zeros, ones, linspace, sin, cos, exp
from numpy.random import random
from numpy.linalg import norm
from .signature import signature, distance as sig_dist, tensor_product
from math import pi

N, d = 81, 2
k = 3
I = linspace(0, 1, N)

a = zeros((N, d))
a[0:N, 0] = [4 * (1 - x) * x for x in I]
a[0:N, 1] = [20 * (x - 1) * (x - 0.5) * x for x in I]
sig_a = signature(a, k)

b = zeros((N, d))
b[0:N, 0] = [sin(x) for x in pi * I]
b[0:N, 1] = [sin(x) for x in 2 * pi * I]
sig_b = signature(b, k)

print(("sig:dist:", sig_dist(a, b, k, d)))

import matplotlib.pyplot as plt

print("plot open.")
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(tensor_product(sig_a, sig_b, d=d, k=k), "yx", label="sig: a x b")
ax.plot(sig_a, "b", label="sig: a")
ax.plot(sig_b, "r", label="sig: a")
ax.legend()

plt.show()
