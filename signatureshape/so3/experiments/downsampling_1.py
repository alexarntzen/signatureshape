import sys

sys.path.append("../../")

from animation.animation_manager import fetch_animations, unpack
import so3.curves as multi
from so3 import animation_to_SO3
import numpy as np
import matplotlib.pyplot as plt
from math import floor


def divisorGenerator(n):
    for i in range(1, n / 4 + 1):
        if n % i == 0:
            yield i


def rounddown(n):
    return int(floor(n / 100) * 100)


print("Load data")
data = fetch_animations(1, description="run")
if not data:
    print("No animations found.")
    sys.exit()


print("Parse data")
s, a, d = unpack(data[0])
c0d = animation_to_SO3(s, a)

print("Calculate distances: ")

fig = plt.figure()
ax = fig.add_subplot(111)
colors = ["r", "b", "y", "g", "m"]

N = c0d.shape[0]
crop = rounddown(c0d.shape[1])
for i in range(N):
    for j in range(N):
        if i <= j:
            continue
        step_arr = []
        dist_arr = []

        for step in divisorGenerator(crop):
            dist = multi.distance(c0d[i], c0d[j], step=step, stop=crop)
            if not np.isnan(dist):
                step_arr.append(step)
                dist_arr.append(dist)
            else:
                ax.plot(
                    [step, step], [0, 10 + (float(i) / crop)], color="k", marker="x"
                )
                break

        ax.plot(step_arr, dist_arr, color=colors[i % 5], marker="o")

plt.show()
