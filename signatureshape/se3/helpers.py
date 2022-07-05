import numpy as np

from so3.helpers import norm as so3_norm

"""
Useful transformations and math helper functions for SE3.
"""
# construct SE3 matrix from rotation matrix R and translation vector t
def assemble_SE3(R, t):
    S = np.eye(4)
    S[0:3, 0:3] = R
    S[0:3, 3] = t
    return S


# Get rotation matrix and translation vector from matrix in SE3
def disassemble_SE3(S):
    return S[0:3, 0:3], S[0:3, 3]


# norm of element in se3 (Lie algebra)
# frobinous norm for hatted isomoprhism and 2 norm are equivalent
def norm(r):
    if r.shape == (4, 4):
        R, t = disassemble_SE3(r)
        return so3_norm(R) + np.norm(r, ord=2)
    return np.norm(r, ord=2)


# I made tis missing function not sure if it is the correct one?
def is_4x4_matrix(q):
    return q.shape[-2:] == (4, 4)


def is_6_vector(q):
    return q.shape[-1:] == (6,)
