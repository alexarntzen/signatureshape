import sys

sys.path.append("../../")
from animation import fetch_animations, unpack
from animation import save_similarity, fetch_animation_id_set, check_already_calucated
from animation.animation_manager import save_signature_se3_distance
from so3.clustering.id_set import get_id_set, crop_curve_based_on_id
from se3.convert import animation_to_SE3
import se3.curves as curves
import se3.transformations as tf
import se3.helpers as hp
import se3.signature as signature
import se3.log_signature as log_signature
from iisignature import prepare

import multiprocessing as mp
import numpy as np
import time

start_time = time.time()
max_frames = 420
min_frames = 130
processes = 12

id_set = get_id_set()
size = len(id_set)

explored = {}
k = 3 - 1
d = 69 * 2
words, word_index = signature.get_words(d, k)
s = prepare(d, k)
print("Finished preperaring")


def similarity(a, b):
    return log_signature.concatenate_metric(a, b, s)
    return log_signature.linear_metric(a, b)
    return signature.inverse_tensor_metric(a, b, words, word_index, k, d)
    return signature.linear_metric(a, b)
    return signature.concatenate_group_metric(a, b, words, word_index, k, d)
    return signature.concatenate_algebra_metric(a, b, words, word_index, k, d)
    return log_signature.concatenate_group_metric(a, b, s)


def explore(id):
    subject, animation, description = unpack(fetch_animations(1, animation_id=id))

    curve_full = animation_to_SE3(subject, animation)
    curve = crop_curve_based_on_id(curve_full, id)
    return curve
    return log_signature.curve_log_signature(curve, s)
    return signature.curve_signature(curve, k)


def worker(i, j):
    a_id = id_set[i]
    b_id = id_set[j]

    if a_id == b_id:
        signature_distance = 0.0
        print(similarity(explored[a_id], explored[b_id]))
    else:
        signature_distance = similarity(explored[a_id], explored[b_id])

    save_signature_se3_distance(a_id, b_id, signature_distance)
    print(
        ("iteration: %d,%d. seconds elapsed: %.2fs." % (i, j, time.time() - start_time))
    )
    return


for i in range(size):
    id = id_set[i]
    explored[id] = explore(id)
    print(("explored: %d. seconds elapsed: %.2fs." % (i, time.time() - start_time)))

if True:
    for i in range(size):
        for j in range(i, size):
            worker(i, j)
else:
    pool = mp.Pool(processes=processes)
    for i in range(size):
        for j in range(i, size):
            pool.apply_async(worker, args=(i, j))

    pool.close()
    pool.join()
