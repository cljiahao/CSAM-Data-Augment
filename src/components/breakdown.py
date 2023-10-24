from tkinter import Label, LabelFrame, PhotoImage
from tkinter import NSEW, SUNKEN

from utils.read_json import read_config, write_config
from utils.widgets import row_col_config
from utils.directory import get_breakdown_qty


class Breakdown():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()
        self.refresh()


    def initialize(self):
        self.config = read_config()
        self.breakdown = {}
        self.previous = {}

    
    def win_config(self):
        pass


    def widgets(self):
        breakdown_frame = LabelFrame(self.root,text="Breakdown of Chips per Category",font=self.config['font']['M_b'])
        row_col_config(breakdown_frame,cols=[0,1,2])
        breakdown_frame.grid(row=0,column=0,pady=(0,5),sticky=NSEW)
        fol_qty = get_breakdown_qty()

        for i,j in enumerate(self.config['breakdown']):
            Label(breakdown_frame,text=j.upper()).grid(row=0,column=i,sticky=NSEW)
            self.breakdown[j] = Label(breakdown_frame,text=fol_qty[j],relief=SUNKEN)
            self.breakdown[j].grid(row=1,column=i,padx=10,sticky=NSEW)
            photo = PhotoImage(file=f'assets/{j}.png')
            photo_display = Label(breakdown_frame,image=photo)
            photo_display.image = photo
            photo_display.grid(row=2,column=i,sticky=NSEW)


    def refresh(self):
        fol_qty = get_breakdown_qty()
        for j in self.config['breakdown']:
            self.breakdown[j].config(text=fol_qty[j])
            if j not in self.previous.keys() or self.previous[j] != fol_qty[j]:
                self.previous[j] = fol_qty[j]
                self.config['breakdown'][j] = fol_qty[j]
                write_config(self.config)
        self.root.after(100,self.refresh)