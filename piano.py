# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
if sys.version_info.major == 2 and sys.version_info.minor == 7 :
    print(sys.version)
    import Tkinter as tk
    import tkFileDialog as filedialog
elif sys.version_info.major == 3 and sys.version_info.minor == 6 :
    print(sys.version)
    import tkinter as tk
    from tkinter import filedialog
else :
    print("Your python version is : ")
    print(sys.version_info.major,sys.version_info.minor)
    print("... I guess it will work !")

import collections

# from Tkinter import Tk,Frame,Button,Label,Scale,IntVar
from observer  import *

import subprocess
##import sys
##sys.path.append("./Sounds")

class Octave(Subject) :
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.degree=degree
        self.set_gamme(degree)
    def set_gamme(self,degree=3) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]="../Sounds/"+key+str(degree)+".wav"
        return self.gamme
    def get_gamme(self) :
        return self.gamme
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)

class Screen(Observer):
    def __init__(self,parent) :
        self.parent=parent
        self.create_screen()
    def create_screen(self) :
        self.screen=tk.Frame(self.parent,borderwidth=5,width=500,height=160,bg="pink")
        self.info=tk.Label(self.screen,text="Appuyez sur une touche clavier ", bg="pink",font=('Arial',10))
        self.info.pack()
    def get_screen(self) :
        return self.screen 
    def update(self,model,key="C") :
        if __debug__:
            if key not in model.gamme.keys()  :
                raise AssertionError    
        subprocess.call(["aplay", model.get_gamme()[key]])
        if self.info :
            self.info.config(text = "Vous avez joue la note : " + key + str(model.get_degree()))

class Keyboard :
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.create_keyboard()        
    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        self.keyboard=tk.Frame(self.parent,borderwidth=5,width=7*key_w,height=key_h,bg="red")
        for key in self.model.gamme.keys() :
            if  key.startswith( '#', 1, len(key) ) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=tk.Button(self.keyboard,name=key.lower(),width=3,height=6, bg = "black")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                if key=="D" and self.model.get_degree() == 3 :
                    button=tk.Button(self.keyboard,name=key.lower(),bg = "grey")
                else :
                    button=tk.Button(self.keyboard,name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1
    def play_note(self,key) :
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees

class Piano :
    def __init__(self,parent,octaves) :
        self.parent=parent
        self.octaves=[]
        self.frame=tk.Frame(self.parent,bg="yellow")
        for octave in range(octaves) :
            self.create_octave(self.frame,octave+2) 
    def create_octave(self,parent,degree=3) :
        frame=tk.Frame(parent,bg="green")
        model=Octave(degree)
        self.octaves.append(model)
        control=Keyboard(frame,model)
        view=Screen(frame)
        model.attach(view)
        view.get_screen().pack()
        control.get_keyboard().pack()
        frame.pack(side="left",fill="x",expand=True)
    def packing(self) :
        self.frame.pack()
      
           
if __name__ == "__main__" :
    root = tk.Tk()
    root.geometry("360x300")
    octaves=2
    root.title("La leçon de piano à "+ str(octaves) + " octaves")
    piano=Piano(root,octaves)
    piano.packing()
    root.mainloop()
