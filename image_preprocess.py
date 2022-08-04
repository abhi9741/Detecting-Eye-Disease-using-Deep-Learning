'''
Preprocess images to
1. remove bg
2. maintain aspect ratio and proportions
'''

import numpy as np
from PIL import Image
import cv2

def trim(img,percentage = 0.02):
    

    w,h = img.size
    img = np.array(img)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert image to gray scale
    img_gray_mean = np.mean(img_gray[img_gray!=0]) #mean pixel value of the non negative pixels
    img_map = img_gray > 0.1*img_gray_mean #pixels that are above 10 percent of the mean value

    print("img map",img_map)
    print("img map size",img_map.size)
    row_sum = np.sum(img_map,axis=1)
    col_sum = np.sum(img_map,axis=0)

    rows = np.where(row_sum>h*percentage)[0] #rows where atleast a certain percentage of pixels are above the threshold (10 percent of the mean)
    cols = np.where(col_sum>w*percentage)[0]

    min_row, min_col = np.min(rows), np.min(cols) #find the first row where atleast a certain percentage of pixels are above the threshold (10 percent of the mean)
    max_row, max_col = np.max(rows), np.max(cols)

    img_trim = img[min_row:max_row+1,min_col:max_col+1] #trim the image so that it only contains rows and columns where atleast a certain percentage of pixels are above the threshold (10 percent of the mean)

    return Image.fromarray(img_trim)

def resize_and_maintain_aspect_ratio(img,output_size):
    input_size = img.size 
    
    ratio = float(output_size)/max(input_size)

    new_size = tuple([int(x*ratio) for x in input_size])
    img_resize = img.resize(new_size,Image.ANTIALIAS)
    img_new = Image.new("RGB",(output_size,output_size))
    img_new.paste(img_resize,((output_size-new_size[0])//2,(output_size-new_size[1])//2))
    
    return img_new

def preprocess_image(args):
    img_file,source_path,dest_path,output_size = args
    # print(args)
    # print(img_file)
    # print(source_path)
    img = Image.open(source_path+img_file)
    #preprocess image
    #trim the image
    print(img)
    img_trim = trim(img)
    #maintain aspect ratio of the image
    img_asp = resize_and_maintain_aspect_ratio(img_trim,output_size[0])
    #save the image
    img_out = img_asp.resize(output_size)
    img_out.save(dest_path+img_file,quality=90)
