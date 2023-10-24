import os
import cv2
import time
import math
import random
from tkinter import Frame, messagebox
from tkinter import BOTH,NSEW
from PIL import Image, ImageTk

from components.base import *
from utils.directory import zip_check_dataset, create_holder
from utils.transfer import grab_images, move_images
from utils.read_json import read_config, write_config
from utils.widgets import row_col_config
from utils.augment import augmenting, templating


class CDA():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()
        self.button_commands()
    

    def initialize(self):
        self.quantity = {}
        self.breakdown = {}
        self.after_id = " "
    

    def win_config(self):
        self.root.state('zoomed')
        self.root.title('CSAM Data Augmentation (CDA)')
        self.h_screen = self.root.winfo_screenheight()
        self.w_screen = self.root.winfo_screenwidth()
        self.frame = Frame(self.root,bg="#33093e")
        row_col_config(self.frame,rows=[5],cols=[0])
        self.frame.pack(fill=BOTH, expand=True)


    def widgets(self):
        
        # Displays
        display_frame = Frame(self.frame,bg="#33093e")
        display_frame.grid(row=0,column=0,rowspan=6,sticky=NSEW)
        row_col_config(display_frame,rows=[0,1],cols=[0])
        self.display = Display(display_frame)

        # Trackbars
        trackbar_frame = Frame(self.frame,bg="#33093e")
        row_col_config(trackbar_frame,cols=[0])
        trackbar_frame.grid(row=0,column=1,ipady=3,sticky=NSEW)
        self.trackbar = Trackbars(trackbar_frame)

        # Buttons
        buttons_frame = Frame(self.frame,bg="#33093e")
        row_col_config(buttons_frame,cols=[0])
        buttons_frame.grid(row=1,column=1,ipady=3,sticky=NSEW)
        self.buttons = Buttons(buttons_frame)

        # Directory
        directory_frame = Frame(self.frame,bg="#33093e")
        row_col_config(directory_frame,cols=[0])
        directory_frame.grid(row=2,column=1,ipady=3,sticky=NSEW)
        self.direct = Directory(directory_frame)
        
        # Quantity_Parameter Frame
        qty_para_frame = Frame(self.frame,bg="#33093e")
        row_col_config(qty_para_frame,rows=[0],cols=[0,1])
        qty_para_frame.grid(row=3,column=1,sticky=NSEW)

        # Quantity
        quantity_frame = Frame(qty_para_frame,bg="#33093e")
        row_col_config(quantity_frame,cols=[0])
        quantity_frame.grid(row=0,column=0,ipady=3,padx=(0,2),sticky=NSEW)
        self.quantity = Quantity(quantity_frame)

        # Parameter
        parameter_frame = Frame(qty_para_frame,bg="#33093e")
        row_col_config(parameter_frame,cols=[0])
        parameter_frame.grid(row=0,column=1,ipady=3,padx=(2,0),sticky=NSEW)
        self.parameter = Parameter(parameter_frame)

        # Breakdown
        breakdown_frame = Frame(self.frame,bg="#33093e")
        row_col_config(breakdown_frame,cols=[0])
        breakdown_frame.grid(row=4,column=1,sticky=NSEW)
        self.breakdown = Breakdown(breakdown_frame)
        

    def button_commands(self):
        self.buttons.random_but.config(command=lambda : self.random_augment())
        self.buttons.reset_but.config(command=lambda : self.reset())
        self.buttons.process_but.config(command=lambda : self.process_augment())


    def random_augment(self):
        breakdown_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"breakdown")

        if len(os.listdir(breakdown_dir)) > 1: breakdown_fols = random.sample(os.listdir(breakdown_dir),2)
        else: breakdown_fols = os.listdir(breakdown_dir)

        img_arr = []
        for i,bd_fol_name in enumerate(breakdown_fols):
            bd_fol_path = os.path.join(breakdown_dir,bd_fol_name)
            img_name = random.sample(os.listdir(bd_fol_path),1)
            img_path = os.path.join(bd_fol_path,img_name[0])
            img_arr.append(img_path)
            self.random_tracking(img_arr)
        

    def random_tracking(self,paths):
        self.display.root.after_cancel(self.after_id)
        for i,path in enumerate(paths):
            mask_def, temp_def = templating(path)
            
            original = Image.open(path)
            self.insert_disp(original,self.display.original[i+1])
            template = Image.fromarray(cv2.cvtColor(temp_def,cv2.COLOR_BGR2RGB))
            self.insert_disp(template,self.display.augment[i+1])
        self.after_id = self.display.root.after(100,self.random_tracking,paths)
            
    
    def insert_disp(self,image,widget):
        image = image.resize((int(image.size[0]*4),int(image.size[1]*4)))
        imgtk = ImageTk.PhotoImage(image = image)
        widget.imgtk = imgtk
        widget.config(image = imgtk)


    def process_augment(self):
        start = time.time()
        try: create_holder()
        except ValueError as e: 
            return messagebox.showerror("Value Error",e)
        print(f"Creating Holder - {time.time()-start}")
        breakdown_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"breakdown")
        mask_arr,temp_arr = [],[]
        for bd_fol_name in os.listdir(breakdown_dir):
            bd_fol_path = os.path.join(breakdown_dir,bd_fol_name)
            for file in os.listdir(bd_fol_path):
                file_path = os.path.join(bd_fol_path,file)
                mask_def, temp_def = templating(file_path)
                mask_arr.append(mask_def)
                temp_arr.append(temp_def)

        print(f"Creating Template - {time.time()-start}")
        dataset_fols = zip_check_dataset(self.direct.dir_dict['output'].get())
        print(f"Zipping Old Datasets - {time.time()-start}")
        augmenting(self.root,mask_arr,temp_arr,dataset_fols)
        print(f"Augmenting Templates - {time.time()-start}")
        self.train_val_split(dataset_fols)
        print(f"Train Test Split - {time.time()-start}")
        return messagebox.showinfo("Processing Completed","Augmentation of NG images completed.")

    
    def train_val_split(self,dataset_fols):
        config = read_config()
        input_dir = config['directories']['input']

        for i in ["good","others"]:

            quantity = config['quantity'][i]
            input_fol = os.path.join(input_dir,i)
            dataset_fol = dataset_fols[f"training_{i}"]
            grab_images(input_fol,dataset_fol,quantity)

        split_perc = float(config['parameter']['validation'])/100

        for j in ["ng","good","others"]:
            train_path = dataset_fols[f"training_{j}"]
            val_path = dataset_fols[f"validation_{j}"]
        
            train_files = os.listdir(train_path)
            split_qty = math.ceil(len(train_files)*split_perc)
            move_images(train_path,val_path,split_qty)


    def reset(self):
        
        config = read_config()
        config['hsv']['current'] = config['hsv']['previous']
        config['mask']['current'] = config['mask']['previous']
        write_config(config)
        
        track_value = self.trackbar.get_values()
        for key,value in self.trackbar.trackbar_text.items():
            for i,txt in enumerate(value):
                self.trackbar.track_dict[key.lower()][txt].set(track_value[key.lower()][i])