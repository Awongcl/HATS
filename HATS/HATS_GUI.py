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

################################################################ Notebook UI ###############################################################################

dacFrame = Frame(my_notebook,width=1080, height=720, background="white")
dacFrame.pack(fill=BOTH,expand = 1)

adcFrame = Frame(my_notebook,width=1080, height=720, background="white")
adcFrame.pack(fill="both",expand = 1)

matrixFrame = Frame(my_notebook,width=1080, height=720, background="white")
matrixFrame.pack(fill="both",expand = 1)

my_notebook.add(dacFrame,text="DAC")
my_notebook.add(adcFrame,text="ADC")
my_notebook.add(matrixFrame,text="Matrix")


############################################################# Wave Gen Functions ############################################################################
def wave():
    wg.generate(shape_variable.get().lower(),int(freuqency.get()))

    dac_text.delete(1.0,END)
    dac_text.insert(END,"Wave Form: ")
    dac_text.insert(END,wg.wave.shape)
    dac_text.insert(END,"\nFrequency: ")
    dac_text.insert(END,wg.wave.freq)

def dac_enable():
    if dac_en.get() == 1:
        dac_text.config(state=NORMAL)
        dac_text.delete(1.0,END)
        dac_text.insert(END, "DAC ready to run.")
    else:
        dac_text.delete(1.0,END)
        dac_text.insert(1.0, "Please enable DAC")
        dac_text.config(state=DISABLED)

#Check button
dac_en = IntVar()
dac_en_cb = Checkbutton(dacFrame,text = "DAC Enable", variable = dac_en,
                 onvalue = 1, offvalue = 0, height=1,width = 20,command=dac_enable)
dac_en_cb.pack(fill=BOTH)
#Labels
Label(dacFrame,text="Wave Form: ").place(x=10,y=50)
Label(dacFrame,text="Frequency: ").place(x=10,y=120)
Label(dacFrame,text="PWM Frequency: ").place(x=600,y=50)
Label(dacFrame,text="Range: 0 - 12.5 mhz ",bg="white").place(x=10,y=150)
#Entry
freuqency = Entry(dacFrame,width=15,bg="white")
freuqency.insert(END,1000)
freuqency.place(x=120,y=120)
#Option menu
shape = ["Sine","Triangle","Square","Sleep"]
shape_variable = StringVar(dacFrame)
shape_variable.set(shape[0])
wave_type = OptionMenu(dacFrame, shape_variable, *shape)
wave_type.place(x=130,y=45)
#Button
generate_wave = Button(dacFrame,text="Generate Waveform",command=wave)
generate_wave.place(x=100,y=250)
#Text
dac_text = Text(dacFrame,height=15, width=30)
dac_text.insert(1.0, "Please enable DAC")
dac_text.configure(state=DISABLED)
dac_text.pack(fill=X,side=BOTTOM)

############################################################# ADC ############################################################################
#Labels
Label(adcFrame,text="ADS1015").place(x=20,y=20)
#Option Menu
GAIN = [6.144,
        4.096,
        2.048,
        1.024,
        0.512,
        0.256]
MULTIPLEXER = []


############################################################# Crosspoint matrix ############################################################################
# Number of rows and columns for ADG2128
rows=8 
columns=12
boxes_1 = []
boxVars_1 = []
boxes_2 = []
boxVars_2 = []
Label(matrixFrame,text="Matrix 1").grid(row=0,column=0)
Label(matrixFrame,text="Matrix 2").grid(row=11,column=0)

for i in range(rows):
    boxVars_1.append([])
    boxVars_2.append([])
    for j in range(columns):
        boxVars_1[i].append(IntVar())
        boxVars_1[i][j].set(0)
        boxVars_2[i].append(IntVar())
        boxVars_2[i][j].set(0)

def getSelected_1():
    selected = []
    for i in range(len(boxVars_1)):
        for j in range(len(boxVars_1[i])):
            if boxVars_1[i][j].get() == 1:
                selected.append([i+1,j+1])
    print(selected)

def getSelected_2():
    selected = []
    for i in range(len(boxVars_2)):
        for j in range(len(boxVars_2[i])):
            if boxVars_2[i][j].get() == 1:
                selected.append([i+1,j+1])
    print(selected)

for x in range(rows):
    boxes_1.append([])
    for y in range(columns):
        Label(matrixFrame, text= "Y %s"%(y+1)).grid(row=0,column=y+1)
        Label(matrixFrame, text= "X %s"%(x+1)).grid(row=x+1,column=0)
        boxes_1[x].append(Checkbutton(matrixFrame, variable = boxVars_1[x][y],onvalue = 1, offvalue = 0, height=1,width = 2))
        boxes_1[x][y].grid(row=x+1, column=y+1)

for x in range(rows):
    boxes_2.append([])
    for y in range(columns):
        Label(matrixFrame, text= "Y %s"%(y+1)).grid(row=11,column=y+1)
        Label(matrixFrame, text= "X %s"%(x+1)).grid(row=x+12,column=0)
        boxes_2[x].append(Checkbutton(matrixFrame, variable = boxVars_2[x][y],onvalue = 1, offvalue = 0, height=1,width = 2))
        boxes_2[x][y].grid(row=x+12, column=y+1)

apply_matrix_1 = Button(matrixFrame, text = "Apply", command = getSelected_1, width = 10)
apply_matrix_1.grid(row = rows+1, column = columns+3)
apply_matrix_2 = Button(matrixFrame, text = "Apply", command = getSelected_2, width = 10)
apply_matrix_2.grid(row = rows+12, column = columns+3)







root.mainloop()

