import sys

sys.path.append("../../")

from animation import fetch_animations, unpack
from so3.convert import animation_to_SO3
import so3.curves as curves
import so3.helpers as hp

import matplotlib.pyplot as plt
import numpy as np
from math import floor


print("Load data")
data = fetch_animations(None, file_name="16_35.amc")

print("Parse data")
s0, a0, d0 = unpack(data)
c0d_demo = hp.crop_curve(animation_to_SO3(s0, a0), stop=160)
c0d_demo = curves.close(c0d_demo, move_origin=True)
N = c0d_demo.shape[1]
I = np.linspace(0, 1, N)
result = [[0], [0], [0]]

if False:
    I_forward = np.linspace(0, 1, N)
    I_backward = np.linspace(0, 1, N)

    for i in range(N / 5):
        I_forward = np.roll(I_forward, 5)
        I_backward = np.roll(I_backward, -5)

        c0d_forward = curves.reparameterize(I_forward, I, c0d_demo)
        c0d_backward = curves.reparameterize(I_backward, I, c0d_demo)
        result[0].append(curves.distance(c0d_forward, c0d_demo))
        result[1].append(curves.distance(c0d_backward, c0d_demo))
        result[2].append(np.linalg.norm(I - I_forward))
else:
    I_forward = np.roll(I, 5)
    I_backward = np.roll(I, -5)
    c0d_forward = c0d_demo.copy()
    c0d_backward = c0d_demo.copy()

    for i in range(N / 5):
        c0d_forward = curves.reparameterize(I_forward, I, c0d_forward)
        c0d_backward = curves.reparameterize(I_backward, I, c0d_backward)
        result[0].append(curves.distance(c0d_forward, c0d_demo))
        result[1].append(curves.distance(c0d_backward, c0d_demo))
        result[2].append(np.linalg.norm(I - np.roll(I, 5 * (i + 1))))

plt.plot(result[0], label="difference forwared shifted reparam and orignal curves.")
plt.plot(result[1], label="difference backward shifted reparam and orignal curves.")
plt.plot(result[2], label="Diffence interval")
plt.legend()
plt.show()
