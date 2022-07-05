from .curves import (
    distance,
    dynamic_distance,
    move_origin_to_zero,
    optimal_reparameterization,
)
from numpy import array, zeros, ones, linspace, sin, cos, exp
from numpy.random import random
from .signature import (
    signature,
    distance as sig_dist,
    tensor_product,
    norm,
    curve_concat_log_metric,
)
from math import pi, pow
from numpy.linalg import norm as np_norm
from iisignature import prepare, sig
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
import matplotlib.pyplot as plt

plt.rc("text", usetex=True)
plt.rc("font", family="serif")
rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"


N, d = 80, 2
K = 40
dt = 1.0 / N

colors = ["b", "g", "r", "y", "c", "k"]


def interpolate(A0, A1, eps=0.0):
    a = zeros((N, d))
    I = array([1, 1])
    for i in range(1, N):
        a[i] = (A0 + eps * I) * dt + a[i - 1]

    return a


def f(I, p):
    return array([pow(i, 1.0 / p) for i in I])


A0 = array([0.5, 0.1])
A1 = array([0.5, 0.1])

print("plot open.")
fig = plt.figure()
plt.suptitle(
    r"Distance calculations for interpolation: $d\left(\left[\begin{array}{c}a_0\\ a_1\end{array}\right]t,\left[\begin{array}{c}a_0+\epsilon \\ a_1\end{array}\right]t\right)$."
)
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 4, projection="3d")
runs = 1000
eps0 = 0.01
I = linspace(eps0, 0, runs)
a = interpolate(A0, A1)
for k in [1, 2, 3, 4]:
    diff = zeros((runs))
    for i in range(runs):
        eps = eps0 * (1 - float(i + 1) / (runs))
        ab = interpolate(A0, A1, eps)
        diff[i] = sig_dist(a, ab, k, d)

    ax1.loglog(I, diff, color=colors[k], label="loglog for degree: %s" % str(k))
    ax1.loglog(I, f(I, k), "--", color=colors[k], label="slope 1/%s" % str(k))
    ax2.plot(I, diff, color=colors[k], label="error degree: %s" % str(k))

ax3.plot(a[:, 0], linspace(0, 1, N), a[:, 1], zdir="z", label=r"$\epsilon = 0.0$")
a = interpolate(A0, A1, 0.1)
ax3.plot(a[:, 0], linspace(0, 1, N), a[:, 1], zdir="z", label=r"$\epsilon = 0.1$")
a = interpolate(A0, A1, 0.2)
ax3.plot(a[:, 0], linspace(0, 1, N), a[:, 1], zdir="z", label=r"$\epsilon = 0.2$")
ax3.set_ylabel("t")
ax3.set_xlabel("x")
ax3.set_zlabel("y")
ax3.legend()
ax3.view_init(elev=20.0, azim=-35)

ax1.legend()
ax2.legend()
ax3.legend()
plt.show()
