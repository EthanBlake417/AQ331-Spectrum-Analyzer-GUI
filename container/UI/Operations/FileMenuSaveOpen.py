from container.UI.Operations.LabelEntry import *
from tkinter import filedialog
import pickle
import os


class FileMenuSaveOpen:
    """
    args: root, scrollable_text_box, input_parameters, save_locations, ports
    performs: Creates file menu, and implements save and open operations
    """
    def __init__(self, root, scrollable_text_box, input_parameters, save_locations, ports, graph_old_data, single_scan):
        """ sets up the menu and initializes some variables"""
        # Initialize
        self.scrollable_text_box = scrollable_text_box
        self.root = root
        self.input_parameters = input_parameters
        self.save_locations = save_locations
        self.ports = ports
        self.graph_old_data = graph_old_data
        self.single_scan = single_scan

        # open defaults
        self.ms_open_defaults()
        self.od_open_defaults()
        self.ss_open_defaults()

        # Create Menu
        my_menu = Menu(root)
        root.config(menu=my_menu)

        # Add File Menu
        file_menu = Menu(my_menu, tearoff=False)
        ms_menu = Menu(my_menu, tearoff=False)
        ss_menu = Menu(my_menu, tearoff=False)
        od_menu = Menu(my_menu, tearoff=False)

        my_menu.add_cascade(label="File", menu=file_menu)
        my_menu.add_cascade(label="Multiple Scans", menu=ms_menu)
        my_menu.add_cascade(label="Single Scan", menu=ss_menu)
        my_menu.add_cascade(label="Graph Old Data", menu=od_menu)

        ms_menu.add_command(label="Save Multiple Scans Configuration", command=self.ms_save_as_file)
        ms_menu.add_command(label="Set Multiple Scans Configuration", command=self.ms_set_defaults)
        ms_menu.add_separator()
        ms_menu.add_command(label="Open Multiple Scans Configuration", command=self.ms_open_file)

        ss_menu.add_command(label="Save Single Scan Configuration", command=self.ss_save_as_file)
        ss_menu.add_command(label="Set Single Scans Configuration", command=self.ss_set_defaults)
        ss_menu.add_separator()
        ss_menu.add_command(label="Open Single Scan Configuration", command=self.ss_open_file)

        od_menu.add_command(label="Save Old Data Configuration", command=self.od_save_as_file)
        od_menu.add_command(label="Set Old Data Configuration", command=self.od_set_defaults)
        od_menu.add_separator()
        od_menu.add_command(label="Open Old Data Configuration", command=self.od_open_file)

        # file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    # Multiple Scans Menu Options
    def ms_save_as_file(self):
        """ Saves the file"""
        list_of_temps, list_of_times = self.scrollable_text_box.get_data()
        save_dict = self.save_locations.get_data()
        port_dict = self.ports.get_data()
        input_parameters_dict = self.input_parameters.get_data()
        wb_file = filedialog.asksaveasfilename(defaultextension=".*",
                                               title="Save File",
                                               filetypes=(("WB files", "*.wb"), ("All Files", "*.*")))
        if wb_file:
            # Save the file
            stuff = {'port_dict': port_dict, 'save_dict': save_dict, 'input_parameters_dict': input_parameters_dict, 'temps': list_of_temps, 'times': list_of_times}
            with open(wb_file, 'wb') as handle:
                pickle.dump(stuff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def ms_open_file(self):
        """ Opens a previously saved file"""
        wb_file = filedialog.askopenfilename(defaultextension=".*",
                                             title="Open File", filetypes=(
                ("WB files", "*.wb"), ("All Files", "*.*")))
        if wb_file:
            # delete old information
            self.save_locations.delete_data()
            self.input_parameters.delete_data()
            self.scrollable_text_box.delete_data()
            self.graph_old_data.delete_data()

            # open the new file
            with open(wb_file, 'rb') as handle:
                saved_data = pickle.load(handle)
            self.save_locations.put_data(**saved_data['save_dict'])
            self.graph_old_data.put_data(**saved_data['save_dict'])
            self.ports.put_data(**saved_data['port_dict'])
            self.input_parameters.put_data(**saved_data['input_parameters_dict'])
            self.scrollable_text_box.put_data(saved_data['temps'], saved_data['times'])

    def ms_set_defaults(self):
        """ Saves the defaults for multiple scans"""
        list_of_temps, list_of_times = self.scrollable_text_box.get_data()
        save_dict = self.save_locations.get_data()
        port_dict = self.ports.get_data()
        input_parameters_dict = self.input_parameters.get_data()
        wb_file = os.path.realpath(r'container\UI\Defaults\multiple_scans.wb')
        # Save the file
        stuff = {'port_dict': port_dict, 'save_dict': save_dict, 'input_parameters_dict': input_parameters_dict, 'temps': list_of_temps, 'times': list_of_times}
        with open(wb_file, 'wb') as handle:
            pickle.dump(stuff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def ms_open_defaults(self):
        """ Opens defaults for multiple scans"""
        wb_file = os.path.abspath(r'container\UI\Defaults\multiple_scans.wb')
        if wb_file:
            # delete old information
            self.save_locations.delete_data()
            self.input_parameters.delete_data()
            self.scrollable_text_box.delete_data()

            # open the new file
            with open(wb_file, 'rb') as handle:
                saved_data = pickle.load(handle)
            self.save_locations.put_data(**saved_data['save_dict'])
            self.ports.put_data(**saved_data['port_dict'])
            self.input_parameters.put_data(**saved_data['input_parameters_dict'])
            self.scrollable_text_box.put_data(saved_data['temps'], saved_data['times'])

    # Single Scan Menu Options
    def ss_save_as_file(self):
        """ Saves the file"""
        single_scan_dict = self.single_scan.get_data()
        wb_file = filedialog.asksaveasfilename(defaultextension=".*",
                                               title="Save File",
                                               filetypes=(("WB files", "*.wb"), ("All Files", "*.*")))
        if wb_file:
            # Save the file
            stuff = {'single_scan_dict': single_scan_dict}
            with open(wb_file, 'wb') as handle:
                pickle.dump(stuff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def ss_open_file(self):
        """ Opens a previously saved file"""
        wb_file = filedialog.askopenfilename(defaultextension=".*",
                                             title="Open File", filetypes=(("WB files", "*.wb"), ("All Files", "*.*")))
        if wb_file:
            # delete old information
            self.single_scan.delete_data()

            # open the new file
            with open(wb_file, 'rb') as handle:
                saved_data = pickle.load(handle)
            self.single_scan.put_data(**saved_data['single_scan_dict'])

    def ss_set_defaults(self):
        """ Saves the defaults for multiple scans"""
        single_scan_dict = self.single_scan.get_data()
        wb_file = os.path.realpath(r'container\UI\Defaults\single_scan.wb')
        # Save the file
        stuff = {'single_scan_dict': single_scan_dict}
        with open(wb_file, 'wb') as handle:
            pickle.dump(stuff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def ss_open_defaults(self):
        """ Opens defaults for multiple scans"""
        wb_file = os.path.abspath(r'container\UI\Defaults\single_scan.wb')
        if wb_file:
            # delete old information
            self.single_scan.delete_data()

            # open the new file
            with open(wb_file, 'rb') as handle:
                saved_data = pickle.load(handle)
            self.single_scan.put_data(**saved_data['single_scan_dict'])

    # Old Data Menu Options
    def od_save_as_file(self):
        """ Saves the file"""
        save_dict = self.graph_old_data.get_data()
        wb_file = filedialog.asksaveasfilename(defaultextension=".*",
                                               title="Save File",
                                               filetypes=(("WB files", "*.wb"), ("All Files", "*.*")))
        if wb_file:
            # Save the file
            stuff = {'save_dict': save_dict}
            with open(wb_file, 'wb') as handle:
                pickle.dump(stuff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def od_open_file(self):
        """ Opens a previously saved file"""
        wb_file = filedialog.askopenfilename(defaultextension=".*",
                                             title="Open File", filetypes=(("WB files", "*.wb"), ("All Files", "*.*")))
        if wb_file:
            # delete old information
            self.graph_old_data.delete_data()

            # open the new file
            with open(wb_file, 'rb') as handle:
                saved_data = pickle.load(handle)
            self.graph_old_data.put_data(**saved_data['save_dict'])

    def od_set_defaults(self):
        """ Saves the defaults for multiple scans"""
        save_dict = self.graph_old_data.get_data()
        wb_file = os.path.abspath(r'container\UI\Defaults\graph_old_data.wb')
        # Save the file
        stuff = {'save_dict': save_dict}
        with open(wb_file, 'wb') as handle:
            pickle.dump(stuff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def od_open_defaults(self):
        """ Opens defaults for multiple scans"""
        wb_file = os.path.realpath(r'container\UI\Defaults\graph_old_data.wb')
        if wb_file:
            # delete old information
            self.graph_old_data.delete_data()

            # open the new file
            with open(wb_file, 'rb') as handle:
                saved_data = pickle.load(handle)
            self.graph_old_data.put_data(**saved_data['save_dict'])


if __name__ == '__main__':
    pass
