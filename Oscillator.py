from tkinter import *
import numpy as np
import sounddevice as sd
import time
from PIL import ImageTk, Image 

root = Tk()
root.geometry("600x400")
root.iconbitmap('keyboard.ico')

canvas = Canvas(root, width = 600, height = 400)      
canvas.place(x=0, y=0)     
img = PhotoImage(file="Mini Oscillator Canvas.png")      
canvas.create_image(0,0, anchor=NW, image=img)
  
sine_img = PhotoImage(file = "sinelogo.png")
saw_img = PhotoImage(file = "sawlogo.png")
square_img = PhotoImage(file = "squarelogo.png")
triangle_img = PhotoImage(file = "trianglelogo.png")

#Volume slider
horizontal = Scale(root, from_=0, to=90, orient=HORIZONTAL, width=6)
horizontal.place(x = 100, y = 300)

notes=Entry(root,width=50, border=4, borderwidth=10)
notes.insert(0,'Enter the note')
notes.place(x=10,y=150)

duration_s=Entry(root,width=50, border=4, borderwidth=10)
duration_s.insert(0,'Duration')
duration_s.place(x=10,y=200)

sample_rate = 96000


def sine():
    freq_Hz = int(notes.get())
    time_sec = int(duration_s.get())
    sample_array = np.arange(sample_rate*time_sec)
    control_vol = float(horizontal.get())
    function = np.sin(2*np.pi*sample_array*freq_Hz/sample_rate)
    red_function = control_vol*function/100
    sine_bits = np.int16(red_function * 32767)
    sd.play(sine_bits, sample_rate)
    time.sleep(time_sec)
    sd.stop()
    

def saw():
    freq_Hz = int(notes.get())
    time_sec = int(duration_s.get())
    sample_array = np.arange(sample_rate*time_sec)
    control_vol = float(horizontal.get())
    def function(n):
        fun = ((2*(-1)**n)/n)*np.sin(2*np.pi*sample_array*freq_Hz*n/sample_rate)
        return fun

    for n in range(1,30):
        x = function(n+1)
        if n == 1:
            y = function(n)
        summ = x+y
        y = summ
    red_wav =  control_vol*y/1000
    saw_bits = np.int16(red_wav * 32767)
    sd.play(saw_bits, sample_rate)
    time.sleep(time_sec)
    sd.stop()
    
def Triangle():
    freq_Hz = int(notes.get())
    time_sec = int(duration_s.get())
    sample_array = np.arange(sample_rate*time_sec)
    control_vol = float(horizontal.get())
    def function(n):
        fun = (2/np.pi)*(((-1)**(n)-1)/n**2)*np.cos(2*np.pi*n*freq_Hz*sample_array/sample_rate)
        return fun

    for n in range(1,30,2):
        x = function(n+2)
        if n == 1:
            y = function(n)
        summ = x+y
        y = summ
    y= y + np.pi/2
    red_wav =  control_vol*y/100
    saw_bits = np.int16(red_wav * 32767)
    sd.play(saw_bits, sample_rate)
    time.sleep(time_sec)
    sd.stop()

def square():
    freq_Hz = int(notes.get())
    time_sec = int(duration_s.get())
    sample_array = np.arange(sample_rate*time_sec)
    control_vol = float(horizontal.get())
    def function(n):
        fun = (4/(np.pi*n))*np.sin(2*np.pi*sample_array*freq_Hz*n/sample_rate)
        return fun

    for n in range(1,31,2):
        x = function(n+2)
        if n == 1:
            y = function(n)
        summ = x+y
        y = summ
    red_wav = control_vol*y/1000
    square_bits = np.int16(red_wav * 32767)
    sd.play(square_bits, sample_rate)
    time.sleep(time_sec)
    sd.stop()


sine_Button = Button(root, text = 'Sine', image = sine_img , command= lambda: sine(),border=0,bg='white')
saw_Button = Button(root, text='Saw', image = saw_img ,command=lambda: saw(), border=0,bg='white')
square_Button = Button(root, text='Square', image = square_img ,command=lambda: square(), border=0,bg='white')
triangle_Button = Button(root, text='Triangle',command=lambda: Triangle(), image = triangle_img, border=0,bg='white')

sine_Button.place(x=400,y=150)
saw_Button.place(x=500,y=150)
square_Button.place(x=400,y=300)
triangle_Button.place(x=500,y=300)


root.mainloop()