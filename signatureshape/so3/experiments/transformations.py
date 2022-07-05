import sys

sys.path.append("../../")

from pylab import *
import so3.transformations as tf
import so3.helpers as hp
import matplotlib.pyplot as plt
from numpy.linalg import norm

n = 1000


# Test whether exp(log(r)) = r
diff_R = zeros(n)
diff_I = zeros(n)
I = eye(3)
lin = linspace(0, 2 * 3.14, n)
for i, v in enumerate(lin):
    R = tf.Ry(v)
    r = tf.rot_log(R)
    diff_R[i] = norm(np.array(tf.rot_exp(r) - R), ord="fro")
    diff_I[i] = norm(np.array(tf.rot_exp(r) - I), ord="fro")

plt.plot(lin, diff_R, label="difference compared to R")
plt.plot(lin, diff_I, label="difference compared to I")
plt.legend()
plt.show()


# Test that the interpolation is linear between R0 and R1
n = 1000
diff_R0 = zeros(n)
diff_R1 = zeros(n)
R0 = tf.Ry(0)
R1 = tf.Ry(2 * 3.14)
for i, v in enumerate(linspace(0, 1, n)):
    r = tf.interpolate(R0, R1, v)
    diff_R0[i] = norm((r - R0), ord="fro")
    diff_R1[i] = norm((r - R1), ord="fro")


plt.plot(lin, diff_R0, label="difference compared to R0")
plt.plot(lin, diff_R1, label="difference compared to R1")
plt.legend()
plt.show()
