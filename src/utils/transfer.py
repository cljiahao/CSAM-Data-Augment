import os
import random
from shutil import rmtree,copyfile,move


def grab_images(input_dir,output_dir,quantity):

    if not os.path.exists(input_dir): raise OSError("Input directory don't exist.")
    if set(os.listdir(os.path.dirname(input_dir))) != set(["ng","good","others"]): raise OSError("Please input the correct input directory.")
    if len(os.listdir(input_dir)) >= int(quantity):
        rmtree(output_dir)
        os.makedirs(output_dir)
        filenames = random.sample(os.listdir(input_dir),int(quantity))
        for file in filenames:
            copyfile(os.path.join(input_dir,file),os.path.join(output_dir,file))
    else: raise ValueError("Input directory file quantity lesser than \nquantity required to process.")


def move_images(input_dir,output_dir,quantity):

    if not os.path.exists(input_dir): raise OSError("Input directory don't exist.")
    if len(os.listdir(input_dir)) >= int(quantity):
        rmtree(output_dir)
        os.makedirs(output_dir)
        filenames = random.sample(os.listdir(input_dir),int(quantity))
        for file in filenames:
            move(os.path.join(input_dir,file),os.path.join(output_dir,file),copy_function=copyfile)
    else: raise ValueError("Input directory file quantity lesser than \nquantity required to process.")