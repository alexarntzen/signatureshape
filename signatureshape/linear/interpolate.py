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
from math import pi
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
k = 5
dt = 1.0 / N


def interpolate(A0, A1, eps=0.0):
    a = zeros((N, d))
    I = array([1, 1])
    for i in range(1, N):
        a[i] = (A0 + eps * I) * dt + a[i - 1]

    return a


A0 = array([0.5, 0.1])
A1 = array([-1.0, 0.0])
runs = 1000
diff = zeros((4, runs))
s = prepare(d, k)

a = interpolate(A0, A1)
for i in range(runs):
    eps = 0.3 * (1 - float(i) / (runs - 1))
    ab = interpolate(A0, A1, eps)
    diff[0, i] = sig_dist(a, ab, k, d)
    diff[1, i] = norm(a, ab, s)
    diff[2, i] = np_norm(a - ab)
    diff[3, i] = curve_concat_log_metric(a, ab, s)


print("plot open.")
fig = plt.figure()
plt.suptitle(
    r"Distance calculations for interpolation: $d\left(\left[\begin{array}{c}a_0\\ a_1\end{array}\right]t,\left[\begin{array}{c}a_0+\epsilon \\ a_1\end{array}\right]t\right)$."
)
ax = fig.add_subplot(2, 1, 1)
I = linspace(0.3, 0, runs)
ax.loglog(I, diff[0, :], "b", label="Inverse signature metric")
ax.loglog(I, diff[1, :], "r", label="Linear log signature norm")
ax.loglog(I, diff[2, :], "g", label="L2 norm between curves")
ax.loglog(I, diff[3, :], "y", label="concatenate")
ax.set_xlabel(r"$\epsilon$")
ax.legend()

ax = fig.add_subplot(2, 1, 2, projection="3d")

ax.plot(a[:, 0], linspace(0, 1, N), a[:, 1], zdir="z", label=r"$\epsilon = 0.0$")
a = interpolate(A0, A1, 0.1)
ax.plot(a[:, 0], linspace(0, 1, N), a[:, 1], zdir="z", label=r"$\epsilon = 0.1$")
a = interpolate(A0, A1, 0.3)
ax.plot(a[:, 0], linspace(0, 1, N), a[:, 1], zdir="z", label=r"$\epsilon = 0.3$")

ax.set_ylabel("t")
ax.set_xlabel("x")
ax.set_zlabel("y")
ax.legend()
ax.view_init(elev=20.0, azim=-35)

plt.show()
