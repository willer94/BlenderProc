import os
import numpy as np
import mathutils
from itertools import product

PI = np.pi
path = '/media/willer/data/BlenderProc/experiments/linemod/camera_position'

def get_random():
	return (np.random.rand()-0.5)*2*PI

D = 2
sample_num = 10000
quaternions = np.random.rand(sample_num, 4)
quaternions = quaternions / np.linalg.norm(quaternions, axis=1, keepdims=True)

ele_num = 10
azi_num = 20
ELEs = [-PI/2+PI/(2*ele_num)*idx for idx in range(ele_num)]
AZIs = [-PI+PI*2/ele_num*idx for idx in range(azi_num)]

ele_azis = np.asarray(list(product(ELEs, AZIs)))

eulers, translations = [], []

#for ele_azi in ele_azis:
for idx in range(sample_num):

	matrix = mathutils.Euler((get_random(), get_random(), get_random())).to_matrix().to_4x4()
	#matrix = mathutils.Euler((-PI/2, 2*PI/10 * idx, (np.random.rand()-0.5)*2*PI/6)).to_matrix().to_4x4()

	#matrix = mathutils.Euler((ele_azi[0], ele_azi[1], 0)).to_matrix().to_4x4()
	matrix.translation = (0, 0, -D)
	matrix = np.linalg.inv(np.asarray(matrix))
	matrix = mathutils.Matrix(matrix)

	# t = -matrix.translation
	# quat = t.to_track_quat('-Z', 'Y').to_euler()	
	# print((-ele_azi[0], 0,-ele_azi[1]), quat)
	# input()

	translations.append(np.asarray(matrix.translation))
	eulers.append(np.asarray(matrix.to_euler()))

eulers, translations = np.stack(eulers), np.stack(translations)

position = np.hstack((translations, eulers))
np.savetxt(path, position, fmt='%.6f')
