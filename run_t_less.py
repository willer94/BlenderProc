import os

models_path = '/media/willer/BackUp/datasets/t_less_model/models_cad_normalized'
models_list = [item for item in os.listdir(models_path) if item.split('.')[-1]=='ply']

workdir = '/media/willer/data/BlenderProc/experiments/t_less'

for m in models_list[:1]:

	m_pth = os.path.join(models_path, m)	
	
	os.system('python run.py %s %s %s %s' % 
		(
			os.path.join(workdir, 'config.yaml'),
			os.path.join(workdir, 'camera_position'),
			m_pth,
			os.path.join(workdir, 'output', m.split('.')[0])
			))
