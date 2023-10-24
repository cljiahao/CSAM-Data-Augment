import os
from tkinter import LabelFrame, Entry
from tkinter import NSEW

from utils.widgets import row_col_config
from utils.read_json import read_config, write_config


class Directory():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()


    def initialize(self):
        self.config = read_config()


    def win_config(self):
        self.reg = (self.root.register(self.callback),'%P','%W')


    def widgets(self):
        input_frame = LabelFrame(self.root,text="Input Directory",font=self.config['font']['M_b'])
        row_col_config(input_frame,cols=[0])
        input_frame.grid(row=0,column=0,sticky=NSEW)
        output_frame = LabelFrame(self.root,text="Output Directory",font=self.config['font']['M_b'])
        row_col_config(output_frame,cols=[0])
        output_frame.grid(row=1,column=0,sticky=NSEW)

        self.dir_dict = {}
        for i,j in enumerate(['Input','Output']):
            frame = LabelFrame(self.root,text=f"{j} Directory",font=self.config['font']['M_b'])
            row_col_config(frame,cols=[0])
            frame.grid(row=i,column=0,sticky=NSEW)
            j = j.lower()
            self.dir_dict[j] = Entry(frame,name=j,font=self.config['font']['M'])
            self.dir_dict[j].insert(0,self.config['directories'][j])
            self.dir_dict[j].config(validate="all",validatecommand=self.reg)
            self.dir_dict[j].grid(row=0,column=0,padx=5,pady=(5,10),sticky=NSEW)


    def callback(self,event,name):
        if name.split(".")[-1] == "input":
            if os.path.exists(event) and set(os.listdir(event)) == set(["ng","good","others"]): 
                self.dir_dict["input"].config(bg='white')
                self.config['directories']['input'] = self.dir_dict["input"].get()
                write_config(self.config)
                return True
        elif name.split(".")[-1] == "output":
            if os.path.exists(event):
                self.dir_dict["output"].config(bg='white')
                self.config['directories']['output'] = self.dir_dict["output"].get()
                write_config(self.config)
                return True
        self.dir_dict[name.split(".")[-1]].config(bg='red')
        return True