from tkinter import filedialog
from container.UI.Operations.tooltips import CreateToolTip
from container.UI.Operations.LabelEntry import *
from container.GraphOldData.slider_old_data import SliderOldData
import pickle
import os
from tkinter import *
from tkinter import ttk
# from queue import Queue
from threading import Thread
import threading
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from tkinter.messagebox import askyesno


class GraphOldData:
    """
    args: root
    sets up a scrollable frame where save locations are put
    """

    def __init__(self, root, tab, tabControl):
        """ sets up a scrollable frame where save locations are put"""
        # initialize
        self.root = root
        self.tab = tab
        # set up tab control
        self.tabControl = tabControl
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text="Old Data Graph")
        # set up for graph
        self.event = threading.Event()
        self.rebuild_canvas_flag = False
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, num="Old Data Spectrum Analysis")  # Create the first figure with two plots
        # set up canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab4)  # A tk.DrawingArea.
        self.canvas.draw()
        # set up toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab4)
        self.toolbar.update()

        # set up scrollable frame
        my_frame = Frame(self.tab, width=350, height=350, bd=1)
        my_frame.place(x=10, y=10)

        canvas = Canvas(my_frame)
        frame = Frame(canvas)
        my_scrollbar = Scrollbar(my_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=my_scrollbar.set)

        my_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=frame, anchor='nw')
        frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=350, height=350))

        # SAVE LOCATION INPUTS
        # HEADER
        Input.label(frame, text="        SAVE LOCATIONS:", row=0, column=0, columnspan=2, font=("Courier", 14))
        # Folder
        Button(frame, text='Choose Spectrum analysis files\nfolder (EMPTY FOLDER):', command=self.pick_folder, width=24, height=2).grid(row=1, column=0, sticky=NW)
        self.output_files_folder = Input.entry(frame, width=27, row=1, column=1, ipady=10, insert="C:")
        # Save location
        Button(frame, text='Choose Final CSV', command=self.open_dialog, width=24, height=2).grid(row=2, column=0, sticky=NW)
        self.final_csv_location = Input.entry(frame, width=27, row=2, column=1, ipady=10, insert="C:")
        # Reference File Location
        Button(frame, text='Choose Reference File Location', command=self.open_reference_file, width=24, height=2).grid(row=3, column=0)
        self.reference_file_location = Input.entry(frame, width=27, row=3, column=1, ipady=10, insert="C:")
        # Create a dictionary where you name each item, as you want it to be referred to in the processes that run:
        self.save_dict = {'output_files_folder': self.output_files_folder, 'final_csv_location': self.final_csv_location, 'reference_file_location': self.reference_file_location}

        # run test button
        button_1 = Button(frame, text='Run Test', bg='green', fg='red', padx=10, pady=5, command=self.run_test)
        button_1.grid(row=4, column=0)

    # These are the functions for choosing folders, etc.
    def pick_folder(self):
        """ opens a directory. this directory must be empty"""
        file = filedialog.askdirectory(title="Choose Folder")
        if file:
            self.output_files_folder.delete(0, END)
            self.output_files_folder.insert(0, file)

    def open_dialog(self):
        """ saves a csv file"""
        file = filedialog.askopenfilename(defaultextension=".*",
                                          title="Open File",
                                          filetypes=(("csv", "*.csv"), ("All Files", "*.*")))
        if file:
            self.final_csv_location.delete(0, END)
            self.final_csv_location.insert(0, file)

    def open_reference_file(self):
        """ opens the reference file"""
        file = filedialog.askopenfilename(defaultextension=".*",
                                          title="Open File",
                                          filetypes=(("csv", "*.csv"), ("All Files", "*.*")))
        if file:
            self.reference_file_location.delete(0, END)
            self.reference_file_location.insert(0, file)

    # these are the getter, setter, and deleting functions
    def get_data(self):
        """ gets save location data"""
        get_data_port_dict = {}
        for key, val in self.save_dict.items():
            get_data_port_dict[key] = val.get()
        return get_data_port_dict

    def delete_data(self):
        """ deletes save location data """
        for val in self.save_dict.values():
            val.delete(0, END)

    def put_data(self, **kwargs):
        """
        action: puts in save location data
        """
        for val, val2 in zip(self.save_dict.values(), kwargs.values()):
            val.insert(0, val2)

    @staticmethod
    def confirm_run_test():
        """ Returns a True Value or a False Value"""
        return askyesno(title='confirmation', message='Are you Sure you want to look at different old data?')

    def run_test(self):
        """ runs the test if you click the run test button"""
        # self.root.withdraw()  # makes user interface window disappear. use root.deiconify() to make it come forward again.
        if self.rebuild_canvas_flag:
            # Confirm Run Test
            if not self.confirm_run_test():
                return
            self.event.set()
            # destroy fig, tab, and canvas
            self.fig.clear()
            self.tab4.destroy()
            # rebuild tab
            self.tab4 = Frame(self.tabControl)
            self.tabControl.add(self.tab4, text="Old Data Graph")
            # rebuild figure
            self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, num="Old Data Spectrum Analysis")  # Create the first figure with two plots
            # rebuild canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab4)  # A tk.DrawingArea.
            self.canvas.draw()
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab4)
            self.toolbar.update()

        # if this flag is set, then we will have to redraw the canvas
        self.rebuild_canvas_flag = True
        # set up args for the separate thread
        animate_freq = 1000000
        save_dict = self.get_data()
        save_dict['freq'] = float(animate_freq)                 # this is just so it won't animate very often
        save_dict['event'] = self.event
        save_dict['fig'] = self.fig
        save_dict['ax1'] = self.ax1
        save_dict['ax2'] = self.ax2
        save_dict['ax3'] = self.ax3
        save_dict['ax4'] = self.ax4
        save_dict['canvas'] = self.canvas

        t1 = Thread(target=SliderOldData, kwargs=save_dict)
        t1.daemon = True            # I'm not sure if this is necessary
        t1.start()

        # switch to new tab
        self.tabControl.select(self.tab4)
        # self.root.destroy()  # makes user interface window end once other windows are exited, so we don't leave rogue processes running


if __name__ == '__main__':
    # set up the widget
    root = Tk()
    root.title("Graph Old Data for SA Testing")
    root.geometry("500x500")
    GraphOldData(root, root)
    root.mainloop()
