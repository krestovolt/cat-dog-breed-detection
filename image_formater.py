import concurrent.futures as cf
from multiprocessing import Pool
import os
import numpy as np
import glob
import sys
import pickle
from tqdm import tqdm
from PIL import Image

'''
utility function for reformat all images from any of extention listed in image_ext
to .jpg format
'''

image_ext = ('*.jpg','*.jpeg','*.png','*.gif')
image_format_to_save = 'jpg'
#original images source
image_data_path = './images/'
#output images folder
save_dir = './data/new_images'
os.makedirs(save_dir, exist_ok=True)

def get_image_label(file_path, separator='_'):
    file_name = os.path.basename(file_path)
    label = '_'.join(file_name.split(separator)[:-1])
    return file_name.split('.')[0],file_name.split('.')[1]

def get_all_images_path():
    imgs = []
    for ext in image_ext:
        imgs.extend(glob.glob(image_data_path+ext))
    return imgs

def run():
    images_path = get_all_images_path()
    size = len(images_path)

    print("processing {} images".format(size))
    temp = None
    # processing image parallel, change processes=YOUR_CPU_CORE
    with Pool(processes=4) as p:
        temp = p.map(process_image, images_path, chunksize=2000)

def process_image(img_path):    
    try:
        imgs = list()
        temp_img = Image.open(img_path)
        img = Image.new('RGB', temp_img.size)
        img.paste(temp_img)

        file_name, orig_ext = get_image_label(img_path)        
        
        img.save('{}/{}.{}'.format(save_dir, file_name, image_format_to_save))

    except Exception as e:
        print("error opening this file => "+img_path)
        print(e)
        return [np.zeros((1, 32, 32, 1), dtype='float32'), 'NONE']


if __name__ == '__main__':
    run()