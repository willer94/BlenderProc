import os

models_path = '/media/willer/BackUp/datasets/OcclusionChallengeICCV2015/models_normalized'
models_list = os.listdir(models_path)
workdir = '/media/willer/data/BlenderProc/experiments/occlusion_linemod'

for m in models_list:

	m_pth = os.path.join(models_path, m)
	if os.path.isdir(m_pth):
		m_name = [item for item in os.listdir(m_pth) if item.split('.')[-1] == 'obj']
		assert len(m_name)==1, 'only one .obj in single file'
		m_name = os.path.join(m_pth, m_name[0])
		os.system('python run.py %s %s %s %s' % 
			(
				os.path.join(workdir, 'config.yaml'),
				os.path.join(workdir, 'camera_position'),
				m_name,
				os.path.join(workdir, 'output', m)
				))
