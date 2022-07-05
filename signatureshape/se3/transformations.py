import numpy as np
from numpy.linalg import norm, inv

import sys

sys.path.append("../")
from so3.transformations import TOL, Rx, Ry, Rz, hat, hatinv, rot_log, rot_exp
from se3.helpers import assemble_SE3, disassemble_SE3, is_4x4_matrix, is_6_vector

# multiply elements in SE3
def rig_dot(S1, S2):
    R1, t1 = disassemble_SE3(S1)
    R2, t2 = disassemble_SE3(S2)
    return assemble_SE3(np.dot(R1, R2), np.dot(R1, t2) + t1)


# inverse of element in SE3
def rig_inv(S):
    R, t = disassemble_SE3(S)
    return assemble_SE3(R.T, -1 * np.dot(R.T, t))


# translation matrix V
def trans_matrix(r):
    theta = norm(hatinv(r))
    if abs(theta) < TOL or np.isinf(theta):
        return np.eye(4)
    return (
        np.eye(3)
        + ((1 - np.cos(theta)) / theta**2) * r
        + ((theta - np.sin(theta)) / theta**3) * np.dot(r, r)
    )


def trans_matrix_inv(w_hat):
    theta = norm(hatinv(w_hat))
    if abs(theta) < TOL or np.isinf(theta):
        return np.eye(3)
    beta = (1 - theta / 2 * np.cos(theta / 2) / np.sin(theta / 2)) / theta**2
    return np.eye(3) - 0.5 * w_hat + beta * w_hat @ w_hat


# From Lie Group SE3 to Lie Algebra se3
def rig_log(S):
    s = np.zeros(6)
    R, t = disassemble_SE3(S)

    w_hat = rot_log(R)
    s[0:3] = trans_matrix_inv(w_hat) @ t
    return s


# From Lie Algebra se3 to Lie Group SE3
def rig_exp(s):
    t = s[0:3]
    r = hat(s[3:6])
    return assemble_SE3(rot_exp(r), np.dot(trans_matrix(r), t))


"""Transformations applied to c in SE3 or q in se3.
c in I->SE3     : n x 4 x 4
c in I->SE3^d   : d x n x 4 x 4

matrix form:
q in I->se3     : n x 4 x 4
q in I->se3^d   : d x n x 4 x 4
matrix for for tangent vectos not implemented yet


vector form:
q in I->se3     : n x 6
q in I->se3^d   : n x 6*d
"""
# right log for descrte curves in gl4
# returns the vector form
def right_log_se3(c, I):
    if len(c.shape) == 4:
        return np.array([right_log_se3(curve, I) for curve in c])

    n_frames = c.shape[0]
    q = np.zeros((n_frames, 6))
    for i in range(n_frames - 1):
        q[i] = rig_log(rig_dot(c[i + 1], rig_inv(c[i]))) / (I[i + 1] - I[i])
    return q


# SRVT:  Imm(I, GL3) -> C(I, gl3\0)
# includes interpolation to godesic by expnential map
# returns the vector form
def SRVT(c, I):
    n_frames = c.shape[0]
    q = np.zeros((n_frames, 6))
    for i in range(n_frames - 1):
        v = rig_log(rig_dot(c[i + 1], rig_inv(c[i]))) / (I[i + 1] - I[i])
        n = norm(v)
        if n < TOL:
            n = 1
        q[i + 1] = v / np.sqrt(n)
    return q


# Calculate R(c0) - R(c1)
def diff_c(c0, c1, I0, I1):
    q0 = SRVT(c0, I0)
    q1 = SRVT(c1, I1)
    return diff_q(q0, q1, I0, I1)


def diff_q(q0, q1, I0, I1):
    if np.array_equal(I0, I1):
        return q0 - q1, I0

    I = np.unique(np.concatenate((I0, I1)))
    diff = multi_interp(I, I0, q0) - multi_interp(I, I1, q1)
    return diff, I


# interpolate a multi dim array on the form fp: R -> R^n
def multi_interp(x, xp, fp):
    return np.stack(
        (np.interp(x, xp, np.array([f[i] for f in fp])) for i in range(fp.shape[1])), -1
    )


# distance between two curves in C(I, so(3)\0)
def distance(c0, c1, I0=None, I1=None):
    # if parameterization not specified we can assume that it is uniform
    if I0 is None:
        I0 = np.linspace(0, 1, c0.shape[0])
    if I1 is None:
        I1 = np.linspace(0, 1, c1.shape[0])

    diff, I = diff_c(c0, c1, I0, I1)
    integrand = np.array([norm(v, ord=2) ** 2 for v in diff])
    return np.sqrt(np.trapz(y=integrand, x=I))


# linearly interpolate between two close points in SO3
def interpolate(S0, S1, s=1):
    return rig_dot(rig_exp(s * rig_log(rig_dot(S1, rig_inv(S0)))), S0)


# reparameterize curve c by linearly interpolating
def reparameterize(I_new, I, c):
    c_new = np.zeros(c.shape)
    # start and end will always be the same
    c_new[0] = c[0]
    c_new[-1] = c[-1]

    j = 0
    for i in range(1, c.shape[0] - 1):
        phi = I_new[i]
        while phi > I[j + 1]:
            j += 1

        s = (phi - I[j]) / (I[j + 1] - I[j])
        c_new[i] = interpolate(c[j], c[j + 1], s)

    return c_new


def concatenate_curve(q):
    if len(q.shape) == 3 and is_6_vector(q):
        d, n, _ = q.shape
        return q.swapaxes(0, 1).reshape(n, 6 * d)
    if len(q.shape) == 2 and is_6_vector(q):
        return q

    raise Exception("Already vectorized in skew_to_vector")


# inverse SRVT: C(I, so3\0) -> C(I, SO3)
# recursivly transform curves in so3^d
def inverse_SRVT(q, I):
    if len(q.shape) == 4:
        return np.array([inverse_SRVT(curve, I) for curve in q])

    n_frames = q.shape[0]
    c = np.zeros((n_frames, 4, 4))
    c[0] = np.eye(4)
    for i in range(n_frames - 1):
        v = (I[i + 1] - I[i]) * norm(q[i]) * q[i]
        c[i + 1] = np.dot(rig_exp(v), c[i])
    return c
