import h5py, numpy as np, os, cv2, tqdm

bg_dir = '/media/willer/BackUp/datasets/SUN2012pascalformat/JPEGImages'
bg_imgs = [os.path.join(bg_dir, item) for item in os.listdir(bg_dir) if item.split('.')[-1] in ['jpg', 'png']]
print('find %d background images' % len(bg_imgs))

h5dir = '/media/willer/data/BlenderProc/experiments/linemod/output/ape'

topath = '/media/willer/BackUp/datasets/linemod_rotate/ape'

if not os.path.exists(topath):
	os.makedirs(topath, exist_ok=True)
	

position = np.loadtxt('/media/willer/data/BlenderProc/experiments/linemod/camera_position', dtype=np.float)

for idx, posi in tqdm.tqdm(enumerate(position[:10], start=0)):
	h5f = '%d.hdf5'%idx

	fi = h5py.File(os.path.join(h5dir, h5f), mode='r')

	rgba = np.asarray(fi.get('colors'))		
	rgb, alpha = rgba[:,:,:3].astype(np.float), rgba[:,:,3].astype(np.float) / 255

	height, width = rgb.shape[:2]
	normal = np.asarray(fi.get('normals'))[:,:,:3]

	bg_img = cv2.imread(np.random.choice(bg_imgs), cv2.IMREAD_COLOR).astype(np.float)
	bg_img = cv2.resize(bg_img, (width, height))

	alpha = alpha[:,:,np.newaxis]
	rgb = np.asarray(rgb* alpha + bg_img*(1-alpha)).astype(np.uint8)
	mask = alpha > 0


	to_fi = h5py.File(os.path.join(topath, h5f), mode='w')
	to_fi.create_dataset('rgb', data=rgb, compression='gzip')
	to_fi.create_dataset('normal', data=normal, compression='gzip')
	to_fi.create_dataset('mask', data=mask, compression='gzip')
	to_fi.create_dataset('position', data=posi, compression='gzip')	
	to_fi.close()