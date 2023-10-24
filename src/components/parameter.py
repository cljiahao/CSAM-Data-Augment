from tkinter import Label, LabelFrame, Entry
from tkinter import NSEW,CENTER,SUNKEN

from utils.read_json import read_config, write_config


class Parameter():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()
        self.refresh()


    def initialize(self):
        self.config = read_config()
        self.parameter = {}
        self.previous = {}
        
    
    def win_config(self):
        self.reg = (self.root.register(self.callback),'%P','%W')


    def widgets(self):
        parameter_frame = LabelFrame(self.root,text="Parameters",font=self.config['font']['M_b'])
        parameter_frame.grid(row=0,column=0,sticky=NSEW)

        for a,b in enumerate(self.config['parameter']):
            if a%2 != 0: a*=2
            Label(parameter_frame,text=b.upper(),font=self.config['font']['S']).grid(row=0,column=a,columnspan=2,sticky=NSEW)

            if a==0:
                self.parameter[b] = Label(parameter_frame,text=1,width=10,justify=CENTER,relief=SUNKEN,font=self.config['font']['S'])
            else:
                self.parameter[b] = Entry(parameter_frame,name=b,width=12,justify=CENTER,font=self.config['font']['S'])
                self.parameter[b].insert(0,self.config['parameter'][b])
                self.parameter[b].config(validate='key',validatecommand=self.reg)
            self.parameter[b].grid(row=1,column=a,pady=3,sticky=NSEW)

            Label(parameter_frame,text="%",font=self.config['font']['S']).grid(row=1,column=a+1,sticky=NSEW)

    
    def callback(self,event,name):
        name = name.split(".")[-1]
        self.config = read_config()
        if str.isdigit(event):
                if 1 <= int(event) <= 100:
                    self.parameter[name].config(bg='white')
                    self.config['parameter'][name] = int(event)
                    write_config(self.config)
                    return True
        self.parameter[name].config(bg='red')
        return True
    

    def refresh(self):
        name = 'randomness'
        self.config = read_config()
        total_qty = sum(self.config['breakdown'].values())
        req_qty = int(self.config['quantity']['ng'])
        randomness = int(100*(total_qty-100)/(req_qty-100))
        
        if name not in self.previous.keys() or self.previous[name] != randomness:
            self.parameter[name].config(text=randomness)
            self.previous[name] = randomness
            self.config['parameter'][name] = randomness
            write_config(self.config)
        self.root.after(1000,self.refresh)