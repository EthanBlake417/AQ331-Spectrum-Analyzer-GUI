import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk #replace with tkinter for python 3
from tkinter import ttk
import numpy as np
from numba import jit
from matplotlib import colors
#maths and display code derived/inspired from Jean Francois Puget
#https://www.ibm.com/developerworks/community/blogs/jfp/entry/My_Christmas_Gift?lang=en


@jit
def mandelbrot(z,maxiter,horizon,log_horizon):
    c = z
    for n in range(maxiter):
        az = abs(z)
        if az > horizon:
            return n - np.log(np.log(az))/np.log(2) + log_horizon
        z = z*z + c
    return 0

@jit
def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
    horizon = 2.0 ** 40
    log_horizon = np.log(np.log(horizon))/np.log(2)
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width,height))
    for i in range(width):
        for j in range(height):
            n3[i,j] = mandelbrot(r1[i] + 1j*r2[j],maxiter,horizon, log_horizon)
    return (r1,r2,n3)

def mandelbrot_image(ax, xmin=-2.,xmax=0.5,ymin=-1.25,ymax=1.25,width=10,height=10,\
             maxiter=1000,cmap='hot',gamma=0.3): #the coords and cmap are essentially a filler for the imput in the plot() function at the bottom of the code


    dpi = 80
    img_width = dpi * width
    img_height = dpi * height
    x,y,z = mandelbrot_set(xmin,xmax,ymin,ymax,img_width,img_height,maxiter)

    ticks = np.arange(0,img_width,3*dpi)
    x_ticks = xmin + (xmax-xmin)*ticks/img_width
    ax.set_xticks(ticks); ax.set_xticklabels(x_ticks)
    y_ticks = ymin + (ymax-ymin)*ticks/img_width
    ax.set_yticks(ticks); ax.set_yticklabels(y_ticks)
    ax.set_title("The Mandelbrot set")
    norm = colors.PowerNorm(gamma)
    ax.imshow(z.T,cmap=cmap,origin='lower',norm=norm)


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)

class base(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Mandelbrot Renderer")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (StartPage, MainPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Lets Begin",
                        command=lambda: controller.show_frame(MainPage))
        button.pack()



class MainPage(tk.Frame):

    def var_states(self):  #this is supposed to send code to run plot() again but it doesnt do it
        print (self.combobox.get())
        print (self.colr)
        self.plot ()


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        values = ['jet', 'rainbow', 'ocean', 'hot', 'cubehelix','gnuplot','terrain','prism', 'pink']
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Re-Render",
                            command=self.plot)
        button2.pack()
        self.mvar = tk.IntVar()
        self.cbutton = tk.Checkbutton(self, text="shadow",onvalue=0, offvalue=1, variable=self.mvar)
        self.cbutton.pack()

        self.combobox = ttk.Combobox(self, values=values)
        self.combobox.current(0)
        self.combobox.pack(side = tk.TOP)

        self.width, self.height = 10, 10
        fig = Figure(figsize=(self.width, self.height))
        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side = tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.plot ()

    def plot (self):
        colr = self.combobox.get()
        print (colr)
        self.ax.clear()
        mandelbrot_image(self.ax, -0.8,-0.7,0,0.1,cmap=colr)
        self.canvas.draw()


app = base()
app.geometry ("800x600")
app.mainloop()