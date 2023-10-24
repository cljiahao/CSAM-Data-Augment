from tkinter import Button, LabelFrame, PhotoImage
from tkinter import NSEW, LEFT

from utils.widgets import row_col_config
from utils.read_json import read_config


class Buttons():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()


    def initialize(self):
        self.config = read_config()
        self.breakdown = {}

    
    def win_config(self):
        self.shuffle_img = PhotoImage(file="assets/shuffle.png")
        self.reset_img = PhotoImage(file="assets/reset.png")
        self.process_img = PhotoImage(file="assets/process.png")

    
    def widgets(self):
        buttons_frame = LabelFrame(self.root)
        row_col_config(buttons_frame,cols=[2])
        buttons_frame.grid(row=0,column=0,sticky=NSEW)
        
        self.random_but = Button(buttons_frame,image=self.shuffle_img,compound=LEFT,text=" Random",font=self.config['font']['M'])
        self.random_but.image = self.shuffle_img
        self.random_but.grid(row=0,column=0,ipadx=10,ipady=7,sticky=NSEW)

        self.reset_but = Button(buttons_frame,image=self.reset_img,compound=LEFT,text=" Reset",font=self.config['font']['M'])
        self.reset_but.image = self.reset_img
        self.reset_but.grid(row=0,column=1,ipadx=10,ipady=7,sticky=NSEW)

        self.process_but = Button(buttons_frame,image=self.process_img,compound=LEFT,text=" Process",font=self.config['font']['M'])
        self.process_but.image = self.process_img
        self.process_but.grid(row=0,column=2,ipadx=10,ipady=7,sticky=NSEW)

        # TODO : Regrab button