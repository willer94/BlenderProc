import os
import numpy as np
import mathutils
from itertools import product

path = '/media/willer/data/BlenderProc/experiments/occlusion_linemod/camera_position'

D = 3
yaw_range   = [0, np.pi*2]
pitch_range = [0, np.pi/2]
roll_range  = [0, np.pi*2]

yaw_num   = 10
pitch_num = 10
roll_num  = 10	

yaws = np.random.uniform(*yaw_range, yaw_num)
pitchs = np.random.uniform(*pitch_range, pitch_num)
rolls = np.random.uniform(*roll_range, roll_num)

p_y_rs = np.stack((pitchs, yaws, rolls)).T

# yaws   = np.linspace(*yaw_range, yaw_num+1)[:-1]
# pitchs = np.linspace(*pitch_range, pitch_num+1)[:-1]
# rolls  = np.linspace(*roll_range, roll_num+1)[:-1]

# p_y_rs = np.asarray(list(product(pitchs, yaws, rolls)))

locations = []
rotations = []
target = mathutils.Vector((0, 0, 0))
for p_y_r in p_y_rs:
	p, y, r = p_y_r.tolist()
	l = np.asarray([
			np.sin(y) * np.cos(p),			
			np.sin(p),
			np.cos(y) * np.cos(p)			
		])
	direction = target - mathutils.Vector(l)
	quat = direction.to_track_quat('-Z', 'Y').to_matrix().to_4x4()
	rollMatrix = mathutils.Matrix.Rotation(r, 4, 'Z')
	euler = (quat * rollMatrix).to_euler()

	locations.append(l)
	rotations.append(euler)

locations = np.stack(locations)
rotations = np.stack(rotations)
locations *= D

l_r = np.hstack((locations, rotations))

l_r = np.around(l_r, decimals=4)
np.savetxt(path, l_r, fmt='%.4f')