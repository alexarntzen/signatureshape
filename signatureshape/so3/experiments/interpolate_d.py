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
data0 = fetch_animations(4, description="run")
data1 = fetch_animations(4, description="walk")

print("Parse data")
s0, a0, d0 = unpack(data0[1])
c0d = animation_to_SO3(s0, a0)

s1, a1, d1 = unpack(data1[1])
c1d = animation_to_SO3(s1, a1)

crop = min(c0d.shape[1], c1d.shape[1])
print(("Crop curves (%d)" % crop))
c0d = curves.crop_curve(c0d, 1, crop)
c1d = curves.crop_curve(c1d, 1, crop)

print("Move origin to zero")
c0d = curves.move_origin_to_zero(c0d)
c1d = curves.move_origin_to_zero(c1d)

print("Interpolate curves")
diff_c0d = []
diff_c1d = []
lin = np.linspace(0, 1, 10)

for s in lin:
    c = curves.interpolate_curves(c0d, c1d, s)
    d0 = curves.distance(c0d, c)
    diff_c0d.append(d0 if not np.isnan(d0) else 0)
    d1 = curves.distance(c1d, c)
    diff_c1d.append(d1 if not np.isnan(d1) else 0)

base = curves.distance(c0d, c1d)
plt.plot([0, 1], [base, base], label="difference c0 and c1")
plt.plot(lin, diff_c0d, label="difference compared to c0")
plt.plot(lin, diff_c1d, label="difference compared to c1")
plt.legend()
plt.show()
