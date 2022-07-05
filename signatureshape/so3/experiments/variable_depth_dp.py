import sys

sys.path.append("../../")

from animation.animation_manager import fetch_animations, unpack
import so3.curves as curves
from so3 import animation_to_SO3
import numpy as np
import matplotlib.pyplot as plt
from math import floor

import time

start_time = time.time()

plt.rc("text", usetex=True)
plt.rc("font", family="serif")

fig = plt.figure()
ax = fig.add_subplot(111)


print("Load data")
data0 = fetch_animations(1, file_name="16_45.amc")
s0, a0, d0 = unpack(data0)
c0d = animation_to_SO3(s0, a0)

data = [fetch_animations(1, file_name="35_26.amc")]
data = data + [fetch_animations(1, file_name="16_58.amc")]
data = data + [fetch_animations(1, file_name="13_11.amc")]
depth_range = list(range(1, 9))
for i in range(len(data)):
    s1, a1, d1 = unpack(data[i])
    c1d = animation_to_SO3(s1, a1)
    dp_arr = [curves.dynamic_distance(c0d, c1d, depth=depth) for depth in depth_range]
    ax.plot(
        depth_range, dp_arr, label=r"$c_0:\mathrm{ %s},c_1:\mathrm{ %s.}$" % (d0, d1)
    )

ax.set_xlabel("depth")
ax.set_ylabel(r"$d_{\mathcal{P}_*}(c_0,c_1\circ\varphi)$")
plt.legend()
plt.show()
