import sys

sys.path.append("../../")

from animation import fetch_animations, unpack
from so3.convert import animation_to_SO3
import so3.curves as curves

import matplotlib.pyplot as plt
import numpy as np


def residue(c):
    if len(c.shape) == 4:
        return sum([np.linalg.norm(e[0] - e[-1], ord="fro") for e in c])


print("Load data")
data0 = fetch_animations(None, file_name="16_35.amc")
data1 = fetch_animations(None, file_name="09_05.amc")

print("Parse data")
s0, a0, d0 = unpack(data0)
c0d = animation_to_SO3(s0, a0)
c0d_demo = animation_to_SO3(s0, a0)

result = [[residue(c0d)], [0]]
for i in range(30):
    c0d = curves.close(c0d, iterations=5, alpha=0.025)
    result[0].append(residue(c0d))
    result[1].append(curves.distance(c0d, c0d_demo))

plt.plot(result[0], label="Residue: norm c[0] - c[-1])")
plt.plot(result[1], label="difference closed and orignal curves.")
plt.legend()
plt.show()
