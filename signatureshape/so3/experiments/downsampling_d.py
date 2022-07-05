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
data = fetch_animations(4, description="walk")
data = data + fetch_animations(4, description="run")
data = data + fetch_animations(4, description="dance")
if not data:
    print("No animations found.")
    sys.exit()


print("Convert to S03")
curves = []
descriptions = []
for i in range(len(data)):
    s, a, d = unpack(data[i])
    if len(a._frames) > 1000:
        curves.append(animation_to_SO3(s, a))
        descriptions.append(d)

size = len(curves)
print(
    (
        "Removed %d from %d animations due to low number of frames."
        % (len(data) - size, len(data))
    )
)

print("Calculate distances")
fig = plt.figure()
ax = fig.add_subplot(111)
colors = ["r", "b", "y", "g", "m"]

for i in range(size):
    c0d = curves[i]
    for j in range(size):
        if i <= j:
            continue
        c1d = curves[j]
        crop = rounddown(min(c0d.shape[1], c1d.shape[1]))
        step_arr = []
        dist_arr = []

        for step in divisorGenerator(crop):
            dist = multi.distance(c0d, c1d, step=step, stop=crop)
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
