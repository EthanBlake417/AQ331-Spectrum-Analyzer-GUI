from tkinter import filedialog
import pyvisa
from tkinter import *
from container.UI.Operations.LabelEntry import Input
from container.SingleReferenceScan.single_scan import spectrum_analyser
from container.UI.Operations.tooltips import CreateToolTip
from tkinter import ttk
import threading
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from tkinter.messagebox import askyesno
import tkinter


class SingleScan:
    """ given a frame, sets up a scrollable frame with input parameters"""

    def __init__(self, root, tab, tabControl, test_currently_running):
        """ sets up the scrollable frame with input parameters"""
        self.root = root
        self.tab = tab
        self.test_currently_running = test_currently_running
        # set up tab control
        self.tabControl = tabControl
        self.tab6 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab6, text="Single Scan Graph")
        # set up for graph
        self.event = threading.Event()
        self.rebuild_canvas_flag = False
        self.fig, self.ax = plt.subplots()  # Create the first figure with two plots
        # set up canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab6)  # A tk.DrawingArea.
        self.canvas.draw()
        # set up toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab6)
        self.toolbar.update()

        # set up scrollable frame
        my_frame = Frame(self.tab, width=350, height=350, bd=1)
        my_frame.place(x=10, y=10)

        canvas = Canvas(my_frame)
        self.frame = Frame(canvas)
        my_scrollbar = Scrollbar(my_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=my_scrollbar.set)

        my_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox("all"), width=350, height=650))

        # FREQ
        Input.label(self.frame, text="SINGLE SCAN:", row=0, column=0, columnspan=1, font=("Courier", 14))

        button_1 = Button(self.frame, text='Run Test', bg='green', fg='red', padx=10, pady=5, command=self.run_test)
        button_1.grid(row=0, column=1, columnspan=1)

        sep = ttk.Separator(self.frame, orient='horizontal')
        sep.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)

        save_location_button = Button(self.frame, text='Choose Save Folder', padx=5, pady=5, command=self.open_dialog)
        save_location_button.grid(row=2, column=0, pady=5)
        self.output_files_folder = Input.entry(self.frame, width=25, row=2, column=1, pady=10, insert="C:")

        Input.label(self.frame, row=3, column=0, text="File Name Addendum:", font=("Courier", 10), pady=5)
        self.addendum = Input.entry(self.frame, width=25, row=3, column=1, pady=10, insert="Type Addendum Here")

        sep2 = ttk.Separator(self.frame, orient='horizontal')
        sep2.grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)

        Input.label(self.frame, row=5, column=0, text="RESOLUTION:")
        self.resolution = Input.entry(self.frame, width=10, row=5, column=1, insert=1)

        Input.label(self.frame, text="CENTER WAVELENGTH (nm):", row=6, column=0)
        self.center_wavelength = Input.entry(self.frame, row=6, column=1, width=10, insert=1310)

        Input.label(self.frame, text="SPAN:", row=7, column=0)
        self.span = Input.entry(self.frame, row=7, column=1, width=10, insert=120)

        Input.label(self.frame, text="Sample Points:", row=8, column=0)
        self.sample_points = Input.entry(self.frame, row=8, column=1, width=10, insert=8000)

        sens_label = Input.label(self.frame, text="Sensitivity:", row=9, column=0)
        CreateToolTip(sens_label, "The options stand for:\nNORM HOLD\nNORM AUTO\nSENS MID\nHIGH1\nHIGH2\nHIGH3\nNote: Anything above HIGH1 might take forever\nAlso: Not sure what SENS MID does.")
        options = ["SNHD", "SNAT", "SMID", "SHI1", "SHI2", "SHI3"]
        self.sensitivity = StringVar(self.frame)
        OptionMenu(self.frame, self.sensitivity, *options).grid(row=9, column=1, sticky=W)
        self.sensitivity.set(options[3])

        sep3 = ttk.Separator(self.frame, orient='horizontal')
        sep3.grid(row=10, column=0, columnspan=2, sticky='ew', pady=10)

        Input.label(self.frame, row=11, column=0, text="SPECTRUM ANALYSIS PORT:")
        self.sa_port = Input.entry(self.frame, width=25, row=11, column=1, insert='GPIB1::7::INSTR')

        check_ports = Button(self.frame, text='CHECK CONNECTED PORTS', padx=10, pady=10, command=self.check_connected_ports)
        check_ports.grid(row=12, column=0, columnspan=2, pady=5)

        # Create a dictionary where you name each item, as you want it to be referred to in the processes that run:
        self.single_scan_dict = {'resolution': self.resolution, 'center_wavelength': self.center_wavelength,
                                 'span': self.span, 'sample_points': self.sample_points, 'sensitivity': self.sensitivity,
                                 'output_files_folder': self.output_files_folder, 'sa_port': self.sa_port, 'addendum': self.addendum}

    # these are the getter, setter, and deleting functions
    def get_data(self):
        """ gets input parameter data"""
        get_data_port_dict = {}
        for key, val in self.single_scan_dict.items():
            if key == 'freq':  # this is to change freq to a float value
                get_data_port_dict[key] = float(val.get())
            else:
                get_data_port_dict[key] = val.get()
        return get_data_port_dict

    def delete_data(self):
        """ deletes input parameter data """
        for val in self.single_scan_dict.values():
            try:
                val.delete(0, END)
            except AttributeError:  # this is for the case of a dropdown menu
                pass

    def put_data(self, **kwargs):
        """
        action: puts in input parameter data
        """
        for key, val in self.single_scan_dict.items():
            for key2, val2 in kwargs.items():
                if key == 'sensitivity' and key2 == 'sensitivity':  # this is for the case of a dropdown menu
                    self.sensitivity.set(val2)
                elif key == key2:
                    val.insert(0, val2)

    def open_dialog(self):
        file = filedialog.askdirectory(title="Choose Folder")
        if file:
            self.output_files_folder.delete(0, END)
            self.output_files_folder.insert(0, file)

    def check_connected_ports(self):
        rm = pyvisa.ResourceManager()
        for i in range(len(rm.list_resources())):
            resources = Text(self.frame, height=1, width=38)
            resources.insert(1.0, rm.list_resources()[i])
            resources.grid(row=(i + 13), column=0, columnspan=2)
            resources.configure(bg=self.frame.cget('bg'), relief="flat")

    @staticmethod
    def confirm_run_test():
        """ Returns a True Value or a False Value"""
        return askyesno(title='confirmation', message='There is Another Test Currently Running,\n are you sure you wish to stop that test and run this one?')

    def run_test(self):
        # self.root.withdraw()  # makes user interface window disappear. use root.deiconify() to make it come forward again.
        if self.test_currently_running.is_set():
            tkinter.messagebox.showwarning("Test Currently Running ", "There is a Test currently Running. You must quit\n that test or wait till it finishes to run a new one. ")
            return
            # if not self.confirm_run_test():
            #     return
        if self.rebuild_canvas_flag:
            self.event.set()
            # destroy fig, tab, and canvas
            self.fig.clear()
            self.tab6.destroy()
            # rebuild tab
            self.tab6 = Frame(self.tabControl)
            self.tabControl.add(self.tab6, text="Single Scan Graph")
            # rebuild figure
            self.fig, self.ax = plt.subplots()  # Create the first figure with two plots
            # rebuild canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab6)  # A tk.DrawingArea.
            self.canvas.draw()
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab6)
            self.toolbar.update()

        # if this flag is set, then we will have to redraw the canvas
        self.rebuild_canvas_flag = True
        # set up args for the separate thread
        single_scan_dict = self.get_data()
        single_scan_dict['event'] = self.event
        single_scan_dict['fig'] = self.fig
        single_scan_dict['ax'] = self.ax
        single_scan_dict['canvas'] = self.canvas
        single_scan_dict['test_currently_running'] = self.test_currently_running
        print(single_scan_dict)

        t3 = threading.Thread(target=spectrum_analyser, kwargs=single_scan_dict)
        t3.daemon = True            # I'm not sure if this is necessary
        t3.start()

        # switch to new tab
        self.tabControl.select(self.tab6)
        # self.root.destroy()  # makes user interface window end once other windows are exited, so we don't leave rogue processes running
        self.test_currently_running.set()

if __name__ == '__main__':
    root = Tk()
    root.title("Spectrum Analysis Single Scan")
    root.geometry("500x800")
    single_scan = SingleScan(root, root)
    root.mainloop()
