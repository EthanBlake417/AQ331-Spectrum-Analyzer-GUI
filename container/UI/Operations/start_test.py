import tkinter
from container.UI.Operations.LabelEntry import *
from tkinter.messagebox import askyesno
from tkinter.messagebox import askyesno
from container.GraphingTool.slider_graphing_tool import GraphSliderData
from container.Oven.oven import EzZone
import time
from container.AQ6331SpectrumAnalyzer.spectrum_analyzer import spectrum_analyser
from container.NewportOpticalPowerMeter1830C.OPM import optical_power_meter
import multiprocessing
from container.UI.Operations.ScrollbarFrame import ScrollbarFrame


class MultipleScans:
    """
    args: root, frame, scrollable_text_box, input_parameters, save_locations, ports
    sets up a scrollable frame, where the start test button is located
    """
    def __init__(self, root, frame, scrollable_text_box, input_parameters, save_locations, ports, test_currently_running):
        """sets up a scrollable frame, where the start test button is located"""
        # Initialize
        self.scrollable_text_box = scrollable_text_box
        self.root = root
        self.frame = frame
        self.input_parameters = input_parameters
        self.save_locations = save_locations
        self.ports = ports

        self.rebuild_canvas_flag = False
        self.test_currently_running = test_currently_running

        # set up scrollable frame
        my_frame = Frame(frame, width=350, height=350, bd=1)
        my_frame.place(x=5, y=5)

        sbf = ScrollbarFrame(my_frame)
        sbf.grid(row=0, column=0, sticky='nsew')
        frame = sbf.scrolled_frame

        # run test button
        button_1 = Button(frame, text='Run Test', bg='green', fg='red', padx=10, pady=5, command=self.run_test)
        button_1.grid(row=0, column=0)

    @staticmethod
    def confirm_run_test():
        """ Returns a True Value or a False Value"""
        return askyesno(title='confirmation', message='There is a Test that is currently Running.\nAre you sure that you want to run this test?\nit may take a few moments to end the other test.')

    def run_test(self):
        """ runs the test if you click the run test button"""
        # Get Data
        list_of_temps, list_of_times = self.scrollable_text_box.get_data()
        save_dict = self.save_locations.get_data()
        port_dict = self.ports.get_data()
        input_parameters_dict = self.input_parameters.get_data()

        kwargs = {**save_dict, **port_dict, **input_parameters_dict, 'list_of_temperatures': list_of_temps, 'list_of_times': list_of_times}
        # Run Test
        if self.test_currently_running.is_set():
            tkinter.messagebox.showwarning("Test Currently Running ", "There is a Test currently Running. You must quit\n that test or wait till it finishes to run a new one. ")
            # if not self.confirm_run_test():
            return
            # stop test:

        # start EZ Zone
        ez = EzZone()
        original_time = time.time()
        print("Beginning Test!")
        # creating processes
        e = multiprocessing.Event()
        oven_flag = multiprocessing.Event()
        opm_flag = multiprocessing.Event()
        ready_to_graph_flag = multiprocessing.Event()

        # add to kwargs
        kwargs['oven_flag'] = oven_flag
        kwargs['opm_flag'] = opm_flag
        kwargs['ready_to_graph_flag'] = ready_to_graph_flag
        kwargs['original_time'] = original_time
        kwargs['e'] = e
        kwargs['test_currently_running'] = self.test_currently_running
        print(kwargs)
        p1 = multiprocessing.Process(target=ez.user_profile, kwargs=kwargs)
        p2 = multiprocessing.Process(target=spectrum_analyser, kwargs=kwargs)
        p3 = multiprocessing.Process(target=optical_power_meter, kwargs=kwargs)
        p4 = multiprocessing.Process(target=GraphSliderData, kwargs=kwargs)

        p1.daemon = True            # I'm not sure if this is necessary
        p2.daemon = True            # I'm not sure if this is necessary
        p3.daemon = True            # I'm not sure if this is necessary
        p4.daemon = True            # I'm not sure if this is necessary

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        # self.root.withdraw()  # makes user interface window disappear. use root.deiconify() to make it come forward again.
        # since I am using kwargs, it is important that these are named, and sent in as kew word arguments
        # StartProcesses(**port_dict, list_of_temperatures=list_of_temps, list_of_times=list_of_times, tabControl=self.tabControl, rebuild_canvas_flag=self.rebuild_canvas_flag, **save_dict, **input_parameters_dict)
        # self.root.destroy()  # makes user interface window end once other windows are exited, so we don't leave rogue processes running
        self.test_currently_running.set()


if __name__ == '__main__':
    pass
