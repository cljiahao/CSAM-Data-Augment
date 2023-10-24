from tkinter import Toplevel, Frame, Label, DoubleVar
from tkinter import NSEW
from tkinter.ttk import Progressbar

from utils.read_json import read_config


class Progress():
    def __init__(self,root) -> None:
        self.root = Toplevel(root)
        self.initialize()
        self.win_config()
        self.widgets()
        self.root.grab_set()


    def initialize(self):
        self.config = read_config()
        
    
    def win_config(self):
        height = int(self.root.winfo_screenheight()*1/3)
        width = int(self.root.winfo_screenwidth()*1/3)
        self.root.geometry(f"{width}x{height}+{width}+{height-100}")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.width = width


    def widgets(self):
        frame = Frame(self.root)
        frame.columnconfigure(0,weight=1)
        frame.rowconfigure(0,weight=1)
        frame.grid(row=0,column=0,sticky=NSEW)

        Label(frame, text="Processing Augmentation to Images. Please wait.",font=self.config['font']['M_b']).grid(row=0,column=0,sticky=NSEW)

        self.progress = 0
        self.progress_var = DoubleVar()
        progress_bar = Progressbar(frame,variable=self.progress_var,length=self.width-30,maximum=100)
        progress_bar.grid(row=1,column=0,ipady=10,pady=50,sticky=NSEW)