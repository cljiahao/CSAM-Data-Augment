from tkinter import Label, LabelFrame, PhotoImage
from tkinter import SUNKEN, NSEW

from utils.widgets import row_col_config


class Display():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()
    
    
    def initialize(self):
        self.display_txt = ["Display 1","Display 2"]
        self.display = {}
        self.original = {}
        self.augment = {}

    
    def win_config(self):
        self.imgtk = PhotoImage(file="assets/arrow.png")


    def widgets(self):

        for i,j in enumerate(self.display_txt):
            key = int(j.split(" ")[-1])
            self.display[key] = LabelFrame(self.root,text=j)
            row_col_config(self.display[key],rows=[0],cols=[0,2])
            self.display[key].grid(row=i,column=0,padx=5,pady=5,sticky=NSEW)

            self.original[key] = Label(self.display[key],relief=SUNKEN)
            self.original[key] .grid(row=0,column=0,padx=5,pady=10,sticky=NSEW)

            arrow_lab = Label(self.display[key], image=self.imgtk)
            arrow_lab.imgtk = self.imgtk
            arrow_lab.grid(row=0,column=1,sticky=NSEW)

            self.augment[key] = Label(self.display[key],relief=SUNKEN)
            self.augment[key].grid(row=0,column=2,padx=5,pady=10,sticky=NSEW)