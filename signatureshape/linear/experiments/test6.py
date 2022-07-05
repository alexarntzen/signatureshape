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

import matplotlib.pyplot as plt

plt.rc("text", usetex=True)
plt.rc("font", family="serif")

yellow = "#FF0000"
blue = "#00A08A"
red = "#F2AD00"
N, d = 81, 1
S, B = 15, 41
I = linspace(0, 1, N)
IS = linspace(-1, 1, S)
IB = linspace(-1, 1, B)

a = zeros((N, d))
a[(S + 1) : (2 * S + 1), 0] = [1 - abs(x) for x in IS]
a[(2 * S) : (3 * S), 0] = [-1 + abs(x) for x in IS]

c = zeros((N, d))
c[(S + B) : (2 * S + B), 0] = [1 - abs(x) for x in IS]

b = zeros((N, d))
b[S : (S + B), 0] = [cos((3.1415 / 2) * x) for x in IB]

# ac_opt  = optimal_reparameterization(a, c, depth = 6)
# bc_opt  = optimal_reparameterization(b, c, depth = 9)


print("plot open.")
fig = plt.figure()
fig.suptitle("Optimal reparameterization for pairs of curves.")
ax = fig.add_subplot(2, 2, 1)
ax.plot(I, a[:, 0], color=red, label=r"$e$")
ax.plot(I, c[:, 0], ":", color=yellow, label=r"$c$")
ax.set_facecolor("#FCFCFC")
ax.legend()
ax = fig.add_subplot(2, 2, 2)
# ax.plot(I, a[:,0], color=red, label=r"$e$")
# ax.plot(I, ac_opt[:,0], ':', color=yellow, label=r"$c\circ\varphi$")
# ax.set_facecolor('#FCFCFC')
# ax.legend()
ax = fig.add_subplot(2, 2, 3)
ax.plot(I, b[:, 0], color=blue, label=r"$f$")
ax.plot(I, c[:, 0], ":", color=yellow, label=r"$c$")
ax.set_facecolor("#FCFCFC")
ax.legend()
ax = fig.add_subplot(2, 2, 4)
# ax.plot(I, b[:,0], color=blue, label=r"$f$")
# ax.plot(I, bc_opt[:,0], ':', color=yellow, label=r"$c\circ\varphi$")
# ax.set_facecolor('#FCFCFC')
# ax.legend()
plt.show()
