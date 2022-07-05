from .src import Animation, Skeleton, parse_asf, parse_amc, mayavi_animate
from .db import (
    get_animation_from_animation_file_name,
    get_subject_from_subject_file_name,
    get_animations_from_subject_description,
    get_animations_from_animation_description,
    get_subject_from_animation_file_name,
)
import pylab as pl
import matplotlib.pyplot as plt
import mayavi.mlab as mlab
import time
import gc
import traceback
import sys
from tvtk.tools import visual

from .src import mayavi_animate

animations = get_animations_from_subject_description("dance")
if not animations:
    print("No animations found.")
    sys.exit()

a_data = animations[0]
a = parse_amc(a_data[1])
a.move_root_to_origin()
print((a_data[0]))
s_data = get_subject_from_animation_file_name(a_data[0])
s = parse_asf(s_data[1])
s.precompute_local_matrices()


# run anim
mayavi_animate(s, a, [0, 0, 0])
