import cv2
import numpy as np

from utils.read_json import read_config


def masking(img):
    config = read_config()

    background = np.where((img[:,:,0]>=130) & (img[:,:,1]>=130) & (img[:,:,2]>=130))
    img[background] = (255,255,255)                             # Convert background to white for better contrast

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    th, ret = cv2.threshold(gray,int(config['mask']['current']['Thresh']),255,cv2.THRESH_BINARY_INV)
    morph = cv2.morphologyEx(ret,cv2.MORPH_CLOSE,(3,3))         # Close off any small poor scannings
    erode = int(config['mask']['current']['Erode'])
    erode = erode if erode%2 == 1 else erode+1
    morph = cv2.morphologyEx(morph,cv2.MORPH_ERODE,np.ones((erode,erode),np.uint8))

    return morph


def get_largest_defect(img, cnts):

    area = 0
    for c in cnts:
        if area < cv2.contourArea(c):
            area = cv2.contourArea(c)
            maxc = c

    blank = np.zeros(img.shape[:2],np.uint8)       
    chipmask = cv2.drawContours(blank,[maxc],-1,(255,255,255),-1)
    chipmask = cv2.dilate(chipmask,np.ones((3,3),np.uint8))
    img[chipmask==0] = [192,192,192]

    return img, chipmask