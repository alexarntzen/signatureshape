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

print("Load data")
data = fetch_animations(None, file_name="16_35.amc")
if not data:
    print("No animations found.")
    sys.exit()

print("Parse data")
s, a, d = unpack(data)
c0d = animation_to_SO3(s, a)
c0d = curves.close(c0d, move_origin=True)

print(("Calculate distances for animation: " + d))

index = 5
c = c0d[index]
c_shift = np.roll(c, -2)
c_shift_2 = np.roll(c, 2)

print("shapes: ", c.shape, c_shift.shape)
print("regular distance:", curves.distance(c, c_shift))
print("regular distance:", curves.dynamic_distance(c, c_shift))
print("regular distance:", curves.dynamic_distance(c, c_shift_2))
