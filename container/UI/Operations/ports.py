import time
from container.UI.Operations.tooltips import CreateToolTip
from container.UI.Operations.LabelEntry import *
from container.UI.Operations.ScrollbarFrame import ScrollbarFrame
from container.UI.Operations.ports_multiprocessing import check_connected_ports_pool
from container.UI.Operations.dropdown import Dropdown
import pyvisa


class Ports:
    """
    args: root
    sets up a scrollable frame where the ports inputs are located
    """
    def __init__(self, root):
        """sets up a scrollable frame where the ports inputs are located"""
        # set up scrollable frame
        my_frame = Frame(root, width=350, height=350, bd=1)
        my_frame.place(x=5, y=5)

        sbf = ScrollbarFrame(my_frame)
        sbf.grid(row=0, column=0, sticky='nsew')
        self.frame = sbf.scrolled_frame

        # port options
        self.options = []
        # Data
        # Ports
        header = Input.label(self.frame, column=0, text="           PORTS:", font=("Courier", 14))
        CreateToolTip(header, "If you get the ports wrong, The test will not work properly. To ensure that the ports are correct, you can turn the instruments on one by one and click the CHECK CONNECTED PORTS button. ")

        quick_check_ports = Button(self.frame, text='QUICK CHECK PORTS', padx=10, pady=10, command=self.quick_check_connected_ports)
        quick_check_ports.grid(row=1, column=0, pady=5, sticky=W)

        detailed_check_ports = Button(self.frame, text='DETAILED CHECK PORTS', padx=10, pady=10, command=self.detailed_check_connected_ports)
        detailed_check_ports.grid(row=1, column=1, pady=5, sticky=W)
        CreateToolTip(detailed_check_ports, "This takes 5-30 seconds, but gives you more information regarding what is connected")

        Input.label(self.frame, row=2, column=0, text="OVEN PORT:")
        self.oven_port = Dropdown(self.frame, options=self.options, row=3, column=0)
        Input.label(self.frame, row=4, column=0, text="SPECTRUM ANALYSIS PORT:")
        self.sa_port = Dropdown(self.frame, options=self.options, row=5, column=0)
        Input.label(self.frame, row=6, column=0, text="OPTICAL POWER METER PORT:")
        self.opm_port = Dropdown(self.frame, options=self.options, row=7, column=0)
        # Create a dictionary where you name each item, as you want it to be referred to in the processes that run
        self.port_dict = {'oven_port': self.oven_port, 'sa_port': self.sa_port, 'opm_port': self.opm_port}

    def quick_check_connected_ports(self):
        rm = pyvisa.ResourceManager()
        self.options = [resource for resource in rm.list_resources()]
        self.reset_port_options()

    def detailed_check_connected_ports(self):
        time0 = time.time()
        # use multiprocessing pool to increase speed of function
        results = check_connected_ports_pool()
        # i = 0
        self.options = []
        for val in results:
            if type(val) == list:
                for message in val:
                    self.options.append(message)
            else:
                self.options.append(val)
        print("Detailed Check Ports Time: ", time.time()-time0)
        self.reset_port_options()

    def reset_port_options(self):
        for val in self.port_dict.values():
            val.reset_values(self.options)

    def get_data(self):
        """ gets ports data """
        get_data_port_dict = {}
        for key, val in self.port_dict.items():
            get_data_port_dict[key] = val.myCombo.get()
        return get_data_port_dict

    def put_data(self, **kwargs):
        """
        action: puts in ports data
        """
        for val, val2 in zip(self.port_dict.values(), kwargs.values()):
            self.options.append(val2)
            val.set_value(val2)


if __name__ == '__main__':
    pass
