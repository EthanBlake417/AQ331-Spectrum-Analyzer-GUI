import multiprocessing
import os
from tkinter import ttk
from mttkinter import mtTkinter
from container.UI.Operations.LabelEntry import *
from container.UI.Operations.scrollable_text_box_class import ScrollableTextBox
from container.UI.Operations.plot_in_tkinter_class import TkinterPlot
from container.UI.Operations.save_locations import SaveLocations
from container.UI.Operations.ports import Ports
from container.UI.Operations.input_parameters import InputParameters
from container.UI.Operations.start_test import MultipleScans
from container.UI.Operations.FileMenuSaveOpen import FileMenuSaveOpen
from container.SingleReferenceScan.single_scan_GUI import SingleScan
from container.GraphOldData.graph_old_data_gui import GraphOldData
import inspect


def start_gui():
    """ This is the GUI portion, that sets up the root and frames, and then starts everything else """
    # make sure the chdir is the same as the one we are using in pycharm
    # os.chdir(os.path.dirname(os.path.abspath(inspect.getsourcefile(inspect.currentframe()))))
    os.chdir(os.path.dirname(__file__))                     # this is a more efficient way to do the same thing
    print("Current Working Directory: ", os.getcwd())
    # set up root window
    root = mtTkinter.Tk()
    root.title("Spectrum Analysis Testing")
    root.geometry("1200x800")
    # set up tabs
    tabControl = ttk.Notebook(root)
    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
    tab3 = Frame(tabControl)

    tabControl.add(tab1, text="Single Scan")
    tabControl.add(tab2, text="Multiple Scans")
    tabControl.add(tab3, text="Graph Old Data")
    tabControl.pack(expand=1, fill='both')

    # set up frames
    frame_1 = Frame(tab2)
    frame_1.place(anchor=NW, height=400, width=400)
    frame_2 = Frame(tab2)
    frame_2.place(anchor=NW, x=400, height=400, width=400)
    frame_3 = Frame(tab2)
    frame_3.place(anchor=NW, x=800, height=400, width=400)
    frame_4 = Frame(tab2)
    frame_4.place(anchor=NW, y=400, height=400, width=400)
    frame_5 = Frame(tab2)
    frame_5.place(anchor=NW, y=400, x=400, height=400, width=400)
    frame_6 = Frame(tab2)
    frame_6.place(anchor=NW, y=400, x=800, height=400, width=400)

    # Test Currently Running flag
    test_currently_running = multiprocessing.Event()

    # scrollable text box
    scrollable_text_box = ScrollableTextBox(frame_1)
    # plotting tool
    TkinterPlot(frame_4, scrollable_text_box)
    # input boxes
    input_boxes = InputParameters(frame_3)
    # save locations
    save_locations = SaveLocations(frame_2)
    # Ports
    ports = Ports(frame_5)
    # Start Test
    multiple_scans = MultipleScans(root, frame_6, scrollable_text_box, input_boxes, save_locations, ports, test_currently_running)

    # tab 2
    single_scan = SingleScan(root, tab1, tabControl, test_currently_running)
    # tab 3
    graph_old_data = GraphOldData(root, tab3, tabControl)
    # File Menu
    FileMenuSaveOpen(root, scrollable_text_box, input_boxes, save_locations, ports, graph_old_data, single_scan)

    root.mainloop()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    start_gui()
