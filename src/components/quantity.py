from tkinter import Label, LabelFrame, Entry
from tkinter import NSEW,CENTER

from utils.read_json import read_config, write_config


class Quantity():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()


    def initialize(self):
        self.config = read_config()
        self.quantity = {}
        
    
    def win_config(self):
        self.reg = (self.root.register(self.callback),'%P','%W')


    def widgets(self):
        quantity_frame = LabelFrame(self.root,text="Quantity per Category",font=self.config['font']['M_b'])
        quantity_frame.grid(row=0,column=0,sticky=NSEW)

        for a,b in enumerate(self.config['quantity']):
            Label(quantity_frame,text=b.upper(),font=self.config['font']['S']).grid(row=0,column=a,sticky=NSEW)
            self.quantity[b] = Entry(quantity_frame,name=b,width=12,justify=CENTER,font=self.config['font']['S'])
            self.quantity[b].insert(0,self.config['quantity'][b])
            self.quantity[b].config(validate='key',validatecommand=self.reg)
            self.quantity[b].grid(row=1,column=a,pady=3)

    
    def callback(self,event,name):
        # TODO: Check if NG and G has the same value or within a specified range of each other
        name = name.split(".")[-1]
        if str.isdigit(event):
            if 1000 <= int(event) or name == "others":
                self.quantity[name].config(bg="white")
                self.config['quantity'][name] = int(event)
                write_config(self.config)
                return True
        self.quantity[name].config(bg="red")
        return True