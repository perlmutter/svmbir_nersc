import os
import time
import argparse
import numpy as np
# from scipy.fft import fft, ifft, fftfreq, fftshift
# import tomopy
# import astra
# import dxchange
import svmbir

if os.environ.get('CLIB') =='CMD_LINE':
    import svmbir.interface_py_c as ci
else:
    import svmbir.interface_cy_c as ci

def run_projector(img_size,num_angles,num_threads=None):
    print(f"Starting size={img_size}x{img_size}")
    img = svmbir.phantom.gen_shepp_logan(img_size,img_size)[np.newaxis]
    angles = np.linspace(0,np.pi,num_angles)
    t0 = time.time()
    tomo = svmbir.project(img, angles, img_size,
                          num_threads=num_threads,
                          verbose=2,
                          svmbir_lib_path='./svmbir_cache')
    t = time.time() - t0
    print(f"Finisehd: time={t}")

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
                                                 svmbir_lib_path='/global/cscratch1/sd/dperl/svmbir_cache2', object_name='object',
                                                 verbose=2)

def sweep_test():
    sizes = [40, 80, 160, 320, 640, 1280, 2560]
    num_angles = [21, 41, 82, 164, 328, 656, 1313]
    t = np.zeros(len(sizes))
    for i,(sz,nang) in enumerate(zip(sizes,num_angles)):
        t0 = time.time()
        cache_system_matrix(sz,nang)
        t[i] = time.time() - t0

    for (sz,nang,tt) in zip(sizes,num_angles,t):
        print(f"{sz}x{sz}-->{nang}x{sz}: {tt} sec")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-s","--img_size",type=int,default=160)
    # parser.add_argument("-a","--num_angles",type=int,default=41)
    # parser.add_argument("-n","--num_threads",type=int,default=1)
    # args = parser.parse_args()
    # # run_projector(args.img_size,args.num_angles)
    # cache_system_matrix(args.img_size,args.num_angles)
    sweep_test()
