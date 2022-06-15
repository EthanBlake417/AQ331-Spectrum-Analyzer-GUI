from container.UI.Operations.tooltips import CreateToolTip
from container.UI.Operations.LabelEntry import *
from container.UI.Operations.ScrollbarFrame import ScrollbarFrame


class InputParameters:
    """ given a frame, sets up a scrollable frame with input parameters"""
    def __init__(self, root):
        """ sets up the scrollable frame with input parameters"""
        # set up scrollable frame
        my_frame = Frame(root, width=350, height=350, bd=1)
        my_frame.place(x=5, y=5)

        sbf = ScrollbarFrame(my_frame)
        sbf.grid(row=0, column=0, sticky='nsew')
        frame = sbf.scrolled_frame

        # FREQ
        Input.label(frame, text="      INPUT PARAMETERS:", row=0, column=0, columnspan=2, font=("Courier", 14))
        freq_label = Input.label(frame, text="FREQ (IN SECONDS):", row=1, column=0)
        CreateToolTip(freq_label,
                      "This describes how often you gather data from the oven and the sensors in seconds.")
        self.freq = Input.entry(frame, row=1, column=1, width=10, insert=10)

        Input.label(frame, row=2, column=0, text="RESOLUTION:")
        self.resolution = Input.entry(frame, width=10, row=2, column=1, insert=1)

        Input.label(frame, text="CENTER WAVELENGTH (nm):", row=3, column=0)
        self.center_wavelength = Input.entry(frame, row=3, column=1, width=10, insert=1310)

        Input.label(frame, text="SPAN:", row=4, column=0)
        self.span = Input.entry(frame, row=4, column=1, width=10, insert=120)

        Input.label(frame, text="Sample Points:", row=5, column=0)
        self.sample_points = Input.entry(frame, row=5, column=1, width=10, insert=8000)

        sens_label = Input.label(frame, text="Sensitivity:", row=6, column=0)
        CreateToolTip(sens_label, "The options stand for:\nNORM HOLD\nNORM AUTO\nSENS MID\nHIGH1\nHIGH2\nHIGH3\nNote: Anything above HIGH1 might take forever\nAlso: Not sure what SENS MID does.")
        options = ["SNHD", "SNAT", "SMID", "SHI1", "SHI2", "SHI3"]
        self.sensitivity = StringVar(frame)
        OptionMenu(frame, self.sensitivity, *options).grid(row=6, column=1, sticky=W)
        self.sensitivity.set(options[3])

        # Create a dictionary where you name each item, as you want it to be referred to in the processes that run:
        self.input_parameters_dict = {'freq': self.freq, 'resolution': self.resolution, 'center_wavelength': self.center_wavelength,
                                      'span': self.span, 'sample_points': self.sample_points, 'sensitivity': self.sensitivity}

    # these are the getter, setter, and deleting functions
    def get_data(self):
        """ gets input parameter data"""
        get_data_port_dict = {}
        for key, val in self.input_parameters_dict.items():
            if key == 'freq':                                   # this is to change freq to a float value
                get_data_port_dict[key] = float(val.get())
            else:
                get_data_port_dict[key] = val.get()
        return get_data_port_dict

    def delete_data(self):
        """ deletes input parameter data """
        for val in self.input_parameters_dict.values():
            try:
                val.delete(0, END)
            except AttributeError:  # this is for the case of a dropdown menu
                pass

    def put_data(self, **kwargs):
        """
        action: puts in input parameter data
        """
        for key, val in self.input_parameters_dict.items():
            for key2, val2 in kwargs.items():
                if key == 'sensitivity' and key2 == 'sensitivity':              # this is for the case of a dropdown menu
                    self.sensitivity.set(val2)
                elif key == key2:
                    val.insert(0, val2)


if __name__ == '__main__':
    pass
