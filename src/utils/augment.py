import os
import cv2
import random
import numpy as np

from components.progress import Progress
from utils.mask import masking, get_largest_defect
from utils.read_json import read_config
from utils.directory import create_holder


def augmenting(root,mask_arr,temp_arr,dataset_fol):

    config = read_config()
    holder_fol = create_holder()
    hold_arr = os.listdir(holder_fol)

    req_qty = len(hold_arr)
    temp_qty = len(mask_arr)
    sample_size = int(req_qty/temp_qty)
    overflow = sample_size//5

    progress_bar = Progress(root)
    progress_step = float(100.0/temp_qty)

    for i,def_mask in enumerate(mask_arr):
        
        rand_elem = random.randrange(1+overflow,sample_size+overflow) if sample_size != 1 else sample_size
        if len(mask_arr)-1 == i: rand_elem = sample_size+overflow
        filenames = random.sample(hold_arr,rand_elem)

        rand_qty = req_qty-rand_elem
        req_qty-=sample_size
        overflow = rand_qty-req_qty if req_qty < rand_qty else sample_size//5

        for f_name in filenames:
            if f_name.split(".")[-1] not in config['img_type']: continue
            img = cv2.imread(os.path.join(holder_fol,f_name))
            chips_mask = masking(img.copy())
            contours, hier = cv2.findContours(chips_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            largest, chip_mask = get_largest_defect(img.copy(),contours)

            mask = cv2.bitwise_and(chip_mask,def_mask)
            img[mask>0] = 0
            img += cv2.bitwise_and(temp_arr[i],temp_arr[i],mask=mask)
            cv2.imwrite(os.path.join(dataset_fol['training_ng'],f"Aug_{i}_{f_name}"),img)
        
        progress_bar.root.update()
        progress_bar.progress += progress_step
        progress_bar.progress_var.set(progress_bar.progress)
    
    progress_bar.root.destroy()


def templating(img_path):

    config = read_config()
    Col_LL = np.array([int(vx) for kx,vx in config['hsv']['current'].items() if kx[0] == "L"], dtype=np.uint8)
    Col_UL = np.array([int(vy) for ky,vy in config['hsv']['current'].items() if ky[0] == "H"], dtype=np.uint8)

    img = cv2.imread(img_path)
    mask = masking(img.copy())
    contours, hier = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    defect, chip_mask = get_largest_defect(img.copy(),contours)

    hsv = cv2.cvtColor(defect,cv2.COLOR_BGR2HSV_FULL)
    mask_def = cv2.inRange(hsv,Col_LL,Col_UL)
    temp_def = cv2.bitwise_and(defect,defect,mask=mask_def)

    return mask_def, temp_def