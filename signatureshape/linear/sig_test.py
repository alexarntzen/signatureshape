from .curves import (
    distance,
    dynamic_distance,
    move_origin_to_zero,
    optimal_reparameterization,
)
from numpy import array, zeros, ones, linspace, sin, cos, exp
from numpy.random import random
from iisignature import sig
from .signature import distance as sig_dist, signature, norm, get_words
from math import pi
from iisignature import prepare

N, D = 81, 2
k = 3
I = linspace(0, 1, N)

a = zeros((N, D))
a[0:N, 0] = [4 * (1 - x) * x for x in I]
a[0:N, 1] = [20 * (x - 1) * (x - 0.5) * x for x in I]
sig_a = signature(a, k)

b = zeros((N, D))
b[0:N, 0] = [sin(x) for x in pi * I]
b[0:N, 1] = [sin(x) for x in 2 * pi * I]
sig_b = signature(b, k)

c = zeros((N, D))
c[0:N, 0] = [sin(x) for x in 2 * pi * I]
c[0:N, 1] = [sin(x) for x in (pi / 2) * I]
sig_c = signature(c, k)

d = zeros((N, D))
d[0:N, 0] = [20 * (x - 1) * (x - 0.5) * x for x in I]
d[0:N, 1] = [4 * (1 - x) * x for x in 0.5 * I]
sig_d = signature(d, k)
depths = [1, 2, 4, 6, 7]
s = prepare(D, k)

# a
ab_dp = array([dynamic_distance(a, b, depth=depth) for depth in depths])
ac_dp = array([dynamic_distance(a, c, depth=depth) for depth in depths])
ad_dp = array([dynamic_distance(a, d, depth=depth) for depth in depths])
dp_fac_a = max([max(ab_dp), max(ac_dp), max(ad_dp)])

ab_norm = array([norm(a, b, s) for depth in depths])
ac_norm = array([norm(a, c, s) for depth in depths])
ad_norm = array([norm(a, d, s) for depth in depths])
norm_fac_a = max([max(ab_norm), max(ac_norm), max(ad_norm)])

ab_sig = array([sig_dist(a, b, k, D) for depth in depths])
ac_sig = array([sig_dist(a, c, k, D) for depth in depths])
ad_sig = array([sig_dist(a, d, k, D) for depth in depths])
sig_fac_a = max([max(ab_sig), max(ac_sig), max(ad_sig)])

# c
ca_dp = array([dynamic_distance(c, a, depth=depth) for depth in depths])
cb_dp = array([dynamic_distance(c, b, depth=depth) for depth in depths])
cd_dp = array([dynamic_distance(c, d, depth=depth) for depth in depths])
dp_fac_c = max([max(ab_dp), max(ac_dp), max(ad_dp)])

ca_norm = array([norm(c, a, s) for depth in depths])
cb_norm = array([norm(c, b, s) for depth in depths])
cd_norm = array([norm(c, d, s) for depth in depths])
norm_fac_c = max([max(ab_norm), max(ac_norm), max(ad_norm)])

print("c + a")
ca_sig = array([sig_dist(c, a, k, D) for depth in depths])
print("c + b")
cb_sig = array([sig_dist(c, b, k, D) for depth in depths])
print("c + d")
cd_sig = array([sig_dist(c, d, k, D) for depth in depths])
sig_fac_c = max([max(ca_sig), max(cb_sig), max(cd_sig)])


pos = [x for x in range(sig_a.shape[0])]
words, _ = get_words(D, k)
labels = [repr(word) for word in words]

import matplotlib.pyplot as plt

print("plot open.")
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(sig_a + 0.0, "b", label="sig: a")
ax.plot(sig_b + 0.0, "r", label="sig: b")
ax.plot(sig_c + 0.0, "g", label="sig: c")
ax.plot(sig_d + 0.0, "y", label="sig: d")
plt.xticks(pos, labels, rotation=-45, fontsize=7)

plt.xlabel("basis element", axes=ax)
plt.ylabel("", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 2, 3)
ax.plot(depths, ab_dp / dp_fac_a, "r", label="dp: a/b")
ax.plot(depths, ac_dp / dp_fac_a, "g", label="dp: a/c")
ax.plot(depths, ad_dp / dp_fac_a, "y", label="dp: a/d")
ax.plot(depths, ab_norm / norm_fac_a, "rx", label="norm: a/b")
ax.plot(depths, ac_norm / norm_fac_a, "gx", label="norm: a/c")
ax.plot(depths, ad_norm / norm_fac_a, "yx", label="norm: a/d")
ax.plot(depths, ab_sig / sig_fac_a, "ro", label="sig_dist: a/b")
ax.plot(depths, ac_sig / sig_fac_a, "go", label="sig_dist: a/c")
ax.plot(depths, ad_sig / sig_fac_a, "yo", label="sig_dist: a/d")
ax.set_ylim((0.0, 1.1))
plt.xlabel("depth of dp", axes=ax)
plt.ylabel("distance", axes=ax)
ax.legend()

ax = fig.add_subplot(2, 2, 4)
ax.plot(depths, ca_dp / dp_fac_c, "b", label="dp: c/a")
ax.plot(depths, cb_dp / dp_fac_c, "r", label="dp: c/b")
ax.plot(depths, cd_dp / dp_fac_c, "y", label="dp: c/d")
ax.plot(depths, ca_norm / norm_fac_c, "bx", label="norm: c/a")
ax.plot(depths, cb_norm / norm_fac_c, "rx", label="norm: c/b")
ax.plot(depths, cd_norm / norm_fac_c, "yx", label="norm: c/d")
ax.plot(depths, ca_sig / sig_fac_c, "bo", label="sig_dist: c/a")
ax.plot(depths, cb_sig / sig_fac_c, "ro", label="sig_dist: c/b")
ax.plot(depths, cd_sig / sig_fac_c, "yo", label="sig_dist: c/d")
ax.set_ylim((0.0, 1.1))
plt.xlabel("depth of dp", axes=ax)
plt.ylabel("distance", axes=ax)
ax.legend()

plt.show()
