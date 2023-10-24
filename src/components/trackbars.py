from tkinter import Label, LabelFrame, Frame, Entry, Button, PhotoImage
from tkinter import NSEW, N, W, HORIZONTAL, END, RIDGE
from tkinter.ttk import Scale

from utils.widgets import row_col_config
from utils.read_json import read_config, write_config


class Trackbars():
    def __init__(self,root) -> None:
        self.root = root
        self.initialize()
        self.win_config()
        self.widgets()


    def initialize(self):
        self.track_value = self.get_values()
        self.tracking = 0
        self.trackbar_text={"HSV": {'Low H': 255,
                                    'High H': 255,
                                    'Low S': 255,
                                    'High S': 255,
                                    'Low V': 255,
                                    'High V': 255},
                            "Mask": {'Thresh': 255,
                                     'Erode': 50}}


    def get_values(self):
        self.config = read_config()
        track_value = {"hsv": [], "mask": []}
        # hsv values
        for col in self.config['hsv']['current'].values(): track_value['hsv'].append(col)
        # mask values
        for a in self.config['mask']['current'].values(): track_value['mask'].append(a)
        
        return track_value
    

    def win_config(self):
        self.expand = PhotoImage(file="assets/expand.png")
        self.expand = self.expand.subsample(2)
        self.reg = (self.root.register(self.callback),'%P','%W')
        
    
    def widgets(self):
        self.track_dict, self.entry_dict = {},{}
        for i,key in enumerate(self.trackbar_text):
            lab_frame = LabelFrame(self.root,text=f"{key} Trackbars",font=self.config['font']['M_b'])
            row_col_config(lab_frame,cols=[0])
            lab_frame.grid(row=i,column=0,sticky=NSEW)

            frame = Frame(lab_frame)
            row_col_config(frame,cols=[2])
            frame.grid(row=1,column=0,sticky=NSEW)
            
            self.track_dict[key.lower()], self.entry_dict[key.lower()] = self.trackbar_loop(frame,key.lower(),self.trackbar_text[key])
            
            expand = Button(lab_frame,image=self.expand,relief=RIDGE,command=lambda frame=frame: self.expand_collapse(frame))
            expand.image = self.expand
            expand.grid(row=0,column=0,padx=5,sticky=N+W)


    def trackbar_loop(self,frame,text_type,text):
        dict_track,dict_entry = {},{}
        for i, txt in enumerate(text):
            dict_track[txt] = Scale(frame,from_=0,to=text[txt],orient=HORIZONTAL)
            dict_track[txt].set(self.track_value[text_type][i])
            dict_track[txt].config(command=lambda event,x=txt,key=text_type: self.insert_values(dict_entry[x],f"{int(float(event))}",key,x))
            dict_track[txt].grid(row=i+1,column=2,padx=10,sticky=NSEW)
            
            Label(frame,font=self.config['font']['M'],text=f"{txt}: ").grid(row=i+1,column=0,padx=5,sticky=W)
           
            dict_entry[txt] = Entry(frame,name=f"{text_type}_{txt}",font=self.config['font']['M'],width=3)
            dict_entry[txt].insert(0,int(dict_track[txt].get()))
            dict_entry[txt].config(validate="key",validatecommand=self.reg)
            dict_entry[txt].grid(row=i+1,column=1,sticky=W)

        return dict_track, dict_entry
    

    def insert_values(self,entry,event,key,txt):
        if event != self.tracking:
            entry.config(validate='none')
            entry.delete(0,END)
            entry.insert(0,event)
            entry.config(validate='key')
            self.config[key]['current'][txt] = event
            write_config(self.config)

    def callback(self,event,name):
        key,txt = name.split(".")[-1].split("_")
        if str.isdigit(event) and len(event)<=3 and int(event) < 256 or event == "":
            track = self.track_dict[key][txt]
            self.tracking = event
            if event == "": track.set(0)
            elif int(track.get()) != event: track.set(int(event))
            self.config[key]['current'][txt] = int(track.get())
            write_config(self.config)
            return True
        else: return False

    
    def expand_collapse(self,frame):
        if frame.grid_info(): frame.grid_forget()
        else: frame.grid(row=1,column=0,sticky=NSEW)