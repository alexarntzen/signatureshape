import sys

sys.path.append("../../")

from animation.animation_manager import fetch_animations, unpack
import so3.curves as multi
from so3 import animation_to_SO3
import numpy as np
import matplotlib.pyplot as plt
from math import floor

import time

start_time = time.time()

print("Load data")
data = fetch_animations(1, animation_id=946)
if not data:
    print("No animations found.")
    sys.exit()

print("Parse data")
s, a, d = unpack(data)
c0d = animation_to_SO3(s, a)

print(("Calculate distances for animation: " + d))
i = 1
N = c0d.shape[0]
dp_arr = []
dist_arr = []
for j in range(N):
    print(("Iteration %d/%d, time: %.3f" % (j + 1, N, (time.time() - start_time))))
    dist = multi.distance(c0d[i], c0d[j])
    dist_arr.append(dist if not np.isnan(dist) else -1)
    dp_dist = multi.dynamic_distance(c0d[i], c0d[j])
    dp_arr.append(dp_dist if not np.isnan(dp_dist) else -1)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(dist_arr)
ax.plot(dp_arr)
plt.show()
