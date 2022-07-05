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
from signature import distance as sig_dist
from math import pi

N, d = 81, 2
I = linspace(0, 1, N)

a = zeros((N, d))
a[0:N, 0] = [4 * (1 - x) * x for x in I]
a[0:N, 1] = [20 * (x - 1) * (x - 0.5) * x for x in I]

b = zeros((N, d))
b[0:N, 0] = [sin(x) for x in pi * I]
b[0:N, 1] = [sin(x) for x in 2 * pi * I]

c = zeros((N, d))
c[0:N, 0] = [sin(x) for x in 2 * pi * I]
c[0:N, 1] = [sin(x) for x in 2 * pi * I]

d = zeros((N, d))
d[0:N, 0] = [20 * (x - 1) * (x - 0.5) * x for x in I]
d[0:N, 1] = [20 * (x - 1) * (x - 0.5) * x for x in I]

dp_distance = [[], [], [], [], []]
sig_distance = [[], [], [], [], []]
runs = 2

for index in range(runs):
    ab_opt = optimal_reparameterization(a, b, depth=index + 1)
    ac_opt = optimal_reparameterization(a, c, depth=index + 1)
    bc_opt = optimal_reparameterization(b, c, depth=index + 1)
    ad_opt = optimal_reparameterization(a, d, depth=index + 1)
    cd_opt = optimal_reparameterization(c, d, depth=index + 1)

    dp_distance[0].append(distance(a, ab_opt))
    dp_distance[1].append(distance(a, ac_opt))
    dp_distance[2].append(distance(b, bc_opt))
    dp_distance[3].append(distance(a, ad_opt))
    dp_distance[4].append(distance(c, cd_opt))

    sig_distance[0].append(sig_dist(a, b, 3))
    sig_distance[1].append(sig_dist(a, c, 3))
    sig_distance[2].append(sig_dist(b, c, 3))
    sig_distance[3].append(sig_dist(a, d, 3))
    sig_distance[4].append(sig_dist(c, d, 3))


import matplotlib.pyplot as plt

print("plot open.")
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(dp_distance[0], "b", label="dp: a/b")
ax.plot(sig_distance[0], "bx", label="sig: a/b")
ax.plot(dp_distance[1], "r", label="dp: a/c")
ax.plot(sig_distance[1], "rx", label="sig: a/c")
ax.plot(dp_distance[2], "g", label="dp: b/c")
ax.plot(sig_distance[2], "gx", label="sig: b/c")
ax.plot(dp_distance[3], "y", label="dp: a/d")
ax.plot(sig_distance[3], "yx", label="sig: a/d")
ax.plot(dp_distance[4], "c", label="dp: c/d")
ax.plot(sig_distance[4], "cx", label="sig: c/d")
plt.xlabel("depth of dp", axes=ax)
plt.ylabel("dynamic distance", axes=ax)
plt.ylim((0, 8))
ax.legend()
plt.show()
