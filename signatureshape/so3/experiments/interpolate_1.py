import sys

sys.path.append("../../")

from animation import fetch_animations, unpack

from so3.convert import animation_to_SO3
import so3.curves as curves
import so3.transformations as tf
import so3.helpers as hp
import matplotlib.pyplot as plt

from math import floor
import numpy as np
from numpy.linalg import det


def divisorGenerator(n):
    for i in range(1, n / 2 + 1):
        if n % i == 0:
            yield i


def getDivisor(n):
    for i in divisorGenerator(n):
        if floor(n / i) < 100:
            return i


def rounddown(n):
    return int(floor(n / 100) * 100)


print("Load data")
data = fetch_animations(1, description="jump")
if not data:
    print("No animations found.")
    sys.exit()

print("Parse data")
s0, a0, d0 = unpack(data[0])

c0d = animation_to_SO3(s0, a0)

c0 = c0d[3]
c1 = c0d[5]
print("Move origin to zero")
c0 = curves.move_origin_to_zero(c0)
c1 = curves.move_origin_to_zero(c1)

print("Interpolate curves")
diff_c0 = []
diff_c1 = []
lin = np.linspace(0, 1, 100)
for s in lin:
    c = curves.interpolate(c0, c1, s)
    diff_c0.append(curves.distance(c0, c))
    diff_c1.append(curves.distance(c1, c))

base = curves.distance(c0, c1)
plt.plot([0, 1], [base, base], label="difference c0 and c1")
plt.plot(lin, diff_c0, label="difference compared to c0")
plt.plot(lin, diff_c1, label="difference compared to c1")
plt.legend()
plt.show()
