#!/usr/bin/python3
import  tkinter as tk
from tkinter import *
from tkinter import ttk
#import driver modules
import wave_gen as wg


root = Tk()
root.title("HATS SYSTEM")
root.geometry("1080x720")

my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=10)

################################################################ Frame UI ###############################################################################

dacFrame = Frame(my_notebook,width=1080, height=720, background="white")
dacFrame.pack(fill=BOTH,expand = 1)

adcFrame = Frame(my_notebook,width=1080, height=720, background="white")
adcFrame.pack(fill="both",expand = 1)


my_notebook.add(dacFrame,text="DAC")
my_notebook.add(adcFrame,text="ADC")


############################################################# Wave Gen Functions ############################################################################
def wave():
    wg.generate(shape_variable.get().lower(),int(freuqency.get()))

    dac_text.delete(1.0,END)
    dac_text.insert(END,"Wave Form: ")
    dac_text.insert(END,wg.wave.shape)
    dac_text.insert(END,"\nFrequency: ")
    dac_text.insert(END,wg.wave.freq)


dac_en = IntVar()
dac_en_cb = Checkbutton(dacFrame,text = "DAC Enable", variable = dac_en,
                 onvalue = 1, offvalue = 0, height=1,
                 width = 20)
dac_en_cb.pack(fill=BOTH)

Label(dacFrame,text="Wave Form: ").place(x=10,y=30)
Label(dacFrame,text="Frequency: ").place(x=10,y=90)
freuqency = Entry(dacFrame,width=10,bg="white")
freuqency.insert(END,1000)
freuqency.place(x=100,y=80)

shape = ["Sine","Triangle","Square","Pause"]
shape_variable = StringVar(dacFrame)
shape_variable.set(shape[0])

wave_type = OptionMenu(dacFrame, shape_variable, *shape)
wave_type.place(x=130,y=30)
generate_wave = Button(dacFrame,text="Generate Waveform",command=wave)
generate_wave.place(x=100,y=200)


Label(dacFrame,text="PWM Frequency: ").place(x=600,y=10)

dac_text = Text(dacFrame,height=15, width=30)
dac_text.pack(fill=X,side=BOTTOM)
dac_text.insert(END, "Just a text Widget\nin two lines\n")








root.mainloop()

