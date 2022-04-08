import os
import time
import argparse
import numpy as np
import svmbir

if os.environ.get('CLIB') =='CMD_LINE':
    import svmbir.interface_py_c as ci
else:
    import svmbir.interface_cy_c as ci

def cache_system_matrix(img_size,num_angles):

    num_slices = 1
    num_rows = img_size
    num_cols = img_size

    angles = np.linspace(0,np.pi,num_angles)
    num_views = len(angles)
    num_channels = img_size
    roi_radius = float(1.0 * max(num_rows, num_cols))/2.0

    paths, sinoparams, imgparams = ci._init_geometry(angles, center_offset=0.0,
                                                 geometry='parallel', dist_source_detector=0.0,
                                                 magnification=1.0,
                                                 num_channels=num_channels, num_views=num_views, num_slices=num_slices,
                                                 num_rows=num_rows, num_cols=num_cols,
                                                 delta_channel=1.0, delta_pixel=1.0,
                                                 roi_radius=roi_radius,
                                                 object_name='object',
                                                 svmbir_lib_path='/global/cscratch1/sd/dperl/svmbir_cache',
                                                 object_name='object',
                                                 verbose=2)

def sweep_test():
    # Increasing img_size/num_angles increases cache file computation time 4x/2x, respectively (also increases cache file size)
    # At img_size/num_angles = 2560/1313, cache file size = 33GB, takes ~13 min on my laptop, but very long time on NERSC (~ 2 hours?)
    sizes = [40, 80, 160, 320, 640]#, 1280, 2560]
    num_angles = [21, 41, 82, 164, 328]#, 656, 1313]
    t = np.zeros(len(sizes))
    for i,(sz,nang) in enumerate(zip(sizes,num_angles)):
        t0 = time.time()
        cache_system_matrix(sz,nang)
        t[i] = time.time() - t0

    for (sz,nang,tt) in zip(sizes,num_angles,t):
        print(f"{sz}x{sz}-->{nang}x{sz}: {tt} sec")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-s","--img_size",type=int,default=160)
    # parser.add_argument("-a","--num_angles",type=int,default=41)
    # args = parser.parse_args()
    # cache_system_matrix(args.img_size,args.num_angles)
    sweep_test()
