import h5py, numpy as np, cv2, os

PATH = 'examples/basic/output'
filelist = os.listdir(PATH)
filelist = [item for item in filelist if item.split('.')[-1] == 'hdf5']

cv2.namedWindow('rgb', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('rgb', 10, 10)
cv2.namedWindow('normal', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('normal', 1000, 10)

for item in filelist:
    f = h5py.File(os.path.join(PATH, item))
    rgb = np.asarray(f.get('colors'), dtype=np.uint8)
    normal = np.asarray(f.get('normals'))
    print('rgb shape: ', rgb.shape, 'rgb range: ' + str(rgb.min()) + ' to ' + str(rgb.max()))
    cv2.imshow('rgb', rgb[:,:,::-1])
    cv2.imshow('normal', normal[:,:,::-1])
    k = cv2.waitKey()
    if k == 27:
        break
