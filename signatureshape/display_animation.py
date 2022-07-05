#!/usr/bin/python
from animation.src.mayavi_animate import mayavi_animate
from animation import fetch_animations, unpack
from so3.convert import animation_to_SO3
import sys

print("Load data")
file_name = sys.argv[1] + "_" + sys.argv[2] + ".amc"
data = fetch_animations(1, file_name=file_name)
if not data:
    print("No animations found.")
    sys.exit()

print("Parse data")
s, a, d = unpack(data)

print("Run animation")
mayavi_animate(s, a, [0, 0, 0])
print(("description: " + d))
c0 = animation_to_SO3(s, a)
print(("animation shape:", c0.shape))
