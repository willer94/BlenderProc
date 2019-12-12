import numpy as np, os

PATH = '/media/willer/data/DataSet/SIXD Chanllenge/T-less/models_cad/'
obj_list = [item for item in os.listdir(PATH) if item.split('.')[-1] == 'ply']

def normal(vertices):
	vertices_mean = np.mean(vertices, axis=0, keepdims=True)
	vertices_ = vertices - vertices_mean
	return vertices_ / np.max(np.abs(vertices_))

for D in obj_list:
	objs = os.path.join(PATH, D)
	print(D)

	with open(objs, 'r') as f:
		model = f.readlines()

	# get v index and v
	# get v and vn by 6 items in a line
	v_idx, v = zip(*[(i, item.strip()) for (i, item) in enumerate(model, start=0) if len(item.split(' '))==6])
	vertices = [item.split(' ')[:3] for item in v]
	vertices = np.asarray([[float(i) for i in item] for item in vertices])
	vertices = normal(vertices)
	vectices = np.around(vertices, decimals=4)

	for idx, v_ in zip(v_idx, vertices):
		v = model[idx]
		v = v.split(' ')
		v[0], v[1], v[2] = str(v_[0]), str(v_[1]), str(v_[2])
		model[idx] = ' '.join(v)

	with open(objs, 'w') as f:
		for l in model:
			f.write(l)
