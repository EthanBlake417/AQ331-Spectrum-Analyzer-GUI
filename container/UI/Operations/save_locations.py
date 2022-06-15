from tkinter import filedialog
from container.UI.Operations.LabelEntry import *
from container.UI.Operations.ScrollbarFrame import ScrollbarFrame


class SaveLocations:
    """
    args: root
    sets up a scrollable frame where save locations are put
    """
    def __init__(self, root):
        """ sets up a scrollable frame where save locations are put"""
        # set up scrollable frame
        my_frame = Frame(root, width=350, height=350, bd=1)
        my_frame.place(x=5, y=5)

        sbf = ScrollbarFrame(my_frame)
        sbf.grid(row=0, column=0, sticky='nsew')
        frame = sbf.scrolled_frame

        # SAVE LOCATION INPUTS
        # HEADER
        Input.label(frame, text="        SAVE LOCATIONS:", row=0, column=0, columnspan=2, font=("Courier", 14))
        # Folder
        Button(frame, text='Choose Spectrum analysis files\nfolder (EMPTY FOLDER):', command=self.pick_folder, width=24, height=2).grid(row=1, column=0, sticky=NW)
        self.output_files_folder = Input.entry(frame, width=27, row=1, column=1, ipady=10, insert="C:")
        # Save location
        Button(frame, text='Save Final CSV', command=self.open_dialog, width=24, height=2).grid(row=2, column=0, sticky=NW)
        self.final_csv_location = Input.entry(frame, width=27, row=2, column=1, ipady=10, insert="C:")
        # Reference File Location
        Button(frame, text='Choose Reference File Location', command=self.open_reference_file, width=24, height=2).grid(row=3, column=0)
        self.reference_file_location = Input.entry(frame, width=27, row=3, column=1, ipady=10, insert="C:")
        # Create a dictionary where you name each item, as you want it to be referred to in the processes that run:
        self.save_dict = {'output_files_folder': self.output_files_folder, 'final_csv_location': self.final_csv_location, 'reference_file_location': self.reference_file_location}

    # These are the functions for choosing folders, etc.
    def pick_folder(self):
        """ opens a directory. this directory must be empty"""
        file = filedialog.askdirectory(title="Choose Folder")
        if file:
            self.output_files_folder.delete(0, END)
            self.output_files_folder.insert(0, file)

    def open_dialog(self):
        """ saves a csv file"""
        file = filedialog.asksaveasfilename(defaultextension=".*",
                                            title="Save File",
                                            filetypes=(("csv", "*.csv"), ("All Files", "*.*")))
        if file:
            self.final_csv_location.delete(0, END)
            self.final_csv_location.insert(0, file)

    def open_reference_file(self):
        """ opens the reference file"""
        file = filedialog.askopenfilename(defaultextension=".*",
                                          title="Save File",
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


if __name__ == '__main__':
    pass

