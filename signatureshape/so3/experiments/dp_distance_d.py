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
data = [fetch_animations(1, file_name="39_02.amc")]
data = data + [fetch_animations(1, file_name="35_26.amc")]
data = data + [fetch_animations(1, file_name="16_35.amc")]
max_frame_count = 180
if not data:
    print("No animations found.")
    sys.exit()

fig = plt.figure()
ax = fig.add_subplot(111)

print("Calculate distances for animations")
size = len(data)
for i in [1]:  # range(size):

    dp_arr = []
    dist_arr = []
    for j in range(size):
        print(("Iteration (%d,%d), time: %.3f" % (i, j, (time.time() - start_time))))
        s0, a0, d0 = unpack(data[i])
        s1, a1, d1 = unpack(data[j])

        c0d = multi.move_origin_to_zero(animation_to_SO3(s0, a0))
        c1d = multi.move_origin_to_zero(animation_to_SO3(s1, a1))
        crop = min(c0d.shape[1], c1d.shape[1], max_frame_count)

        # calculate distances
        dist = multi.distance(c0d[i], c0d[j])
        dist_arr.append(dist if not np.isnan(dist) else -1)
        dp_dist = multi.dynamic_distance(c0d[i], c0d[j])
        dp_arr.append(dp_dist if not np.isnan(dp_dist) else -1)

    # plot results
    ax.plot(dist_arr)
    ax.plot(dp_arr)


plt.show()
