import numpy as np, os

PATH = '/media/willer/software/dataset/YCB/models'
toPATH = '/media/willer/software/dataset/YCB/models_normalized'
dir_list = os.listdir(PATH)

def normal(vertices):
	vertices_max = np.max(vertices, axis=0, keepdims=True)
	vertices_min = np.min(vertices, axis=0, keepdims=True)

	vertices_mean = (vertices_max + vertices_min) / 2.
	print(vertices_max, vertices_min, vertices_mean)
	vertices_ = vertices - vertices_mean
	return vertices_ / np.max(np.abs(vertices_))

#dir_list = [item for item in dir_list if 'pudding' in item]
for D in dir_list:		
	if os.path.isdir(os.path.join(PATH, D)):
		print(D)
		objs = [item for item in os.listdir(os.path.join(PATH, D)) if item.split('.')[-1] == 'obj']
		obj = os.path.join(PATH, D, objs[0])
		with open(obj, 'r') as f:
			model = f.readlines()

		# get v index and v
		v_idx, v = zip(*[(i, item.strip()) for (i, item) in enumerate(model, start=0) if item.split(' ')[0]=='v'])
		vertices = [item.split(' ')[1:4] for item in v]
		vertices = np.asarray([[float(i) for i in item] for item in vertices])
		vertices = normal(vertices)
		vectices = np.around(vertices, decimals=6)

		for idx, v_ in zip(v_idx, vertices):
			v = model[idx]
			v = v.split(' ')
			v[1], v[2], v[3] = '%.6f'%v_[0], '%.6f'%v_[1], '%.6f'%v_[2]
			model[idx] = ' '.join(v)
			model[idx] += '\n'

		with open(os.path.join(toPATH, D, objs[0]), 'w') as f:
			for l in model:
				f.write(l)
