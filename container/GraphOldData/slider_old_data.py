import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
import pandas as pd
import os.path
from matplotlib.animation import FuncAnimation
import numpy as np
from contextlib import suppress
import tkinter
import os


class SliderOldData:
    def __init__(self, freq, output_files_folder, final_csv_location, reference_file_location, event, fig, ax1, ax2, ax3, ax4, canvas):
        # more initializing
        self.fig, self.ax1, self.ax2, self.ax3, self.ax4, self.canvas = fig, ax1, ax2, ax3, ax4, canvas
        self.event = event
        # initialize parameters
        self.freq, self.output_files_folder, self.final_csv_location, self.reference_file_location = freq, output_files_folder, final_csv_location, reference_file_location

        # initialize self.get_data
        self.min_list, self.opm_time, self.opm_reading, self.oven_time, self.cur_temp, self.setpoint_temp, self.mean_wavelength_time, self.mean_wavelength, self.total_power = 0, [], None, [], None, None, None, None, None
        # initialize self.calculate some things
        self.files, self.number_of_files, self.minimum_index, self.maximum_index, self.minimum_spectrum, self.maximum_spectrum = [], None, None, None, None, None
        # get data and basic set up

        self.get_data(output_files_folder, final_csv_location)  # updates: self.min_list, self.opm_time, self.opm_reading, self.oven_time, self.cur_temp, self.setpoint_temp, self.mean_wavelength_time, self.mean_wavelength, self.total_power
        self.calculate_some_things(output_files_folder)  # updates: self.files, self.number_of_files, self.minimum_index, self.maximum_index, self.minimum_spectrum, self.maximum_spectrum

        # reference file data
        self.reference_light_level = pd.read_csv(reference_file_location)["light_level"].tolist()
        self.reference_mean_wavelength = pd.read_csv(reference_file_location)["mean_wavelength"].tolist()[0]
        try:
            self.reference_power_level = pd.read_csv(reference_file_location)["total_power"].tolist()[0]
        except KeyError:
            self.reference_power_level = [0]
            print("Reference Power Level Data is Missing!")

        # create subtracted data
        self.subtracted_light_level = None
        self.create_subtracted_data()  # updates: self.subtracted_light_level

        # set up figures
        self.fig.subplots_adjust(hspace=.3, wspace=.262)

        # set up plots
        self.ax1_twin, self.spectrum_analysis_ref, self.spectrum_analysis, self.subtracted_scan = None, None, None, None
        self.ax2_twin, self.plot2, self.plot2_total_power, self.plot2_line, self.plot2_reference = None, None, None, None, None
        self.plot3_cur, self.plot3_setpoint, self.plot3_line = None, None, None
        self.plot4, self.plot4_reference, self.plot4_line = None, None, None
        self.plot_1()  # sets up the first plot and updates: self.ax1_twin, self.spectrum_analysis_ref, self.spectrum_analysis, self.subtracted_scan
        self.plot_2()  # sets up the second plot and updates: self.ax2_twin, self.plot2, self.plot2_total_power, self.plot2_line
        self.plot_3()  # sets up the third plot and updates: self.plot3_cur, self.plot3_setpoint, self.plot3_line
        self.plot_4()  # sets up the fourth plot and updates: self.plot4, self.plot4_reference, self.plot4_line

        # slider function
        slider_loc = plt.axes([0.16, 0.05, 0.7, 0.04])
        self.slider = Slider(slider_loc, 'File', valmin=1, valmax=2, valinit=2, valstep=1)
        self.animate_spectrum_analyzer()        # this will update to the appropriate starting values for the slider
        self.slider.on_changed(self.update)
        # animation function
        self.a = FuncAnimation(self.fig, self.animate, interval=(freq * 1000))

        # update canvas
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def plot_1(self):
        self.ax1_twin = self.ax1.twinx()
        self.ax1_twin.set_ylabel("Difference")
        self.ax1.set_title("Date/Time Temperature Power Level")
        self.ax1.set_xlim(self.minimum_index, self.maximum_index)
        self.ax1.set_ylim(-75, -25)
        self.ax1.set_ylabel("Light Level")
        self.ax1.set_xlabel("Wavelength")
        plt.subplots_adjust(bottom=0.2)
        # set up plot for spectrum analysis
        wavelength_axis = pd.read_csv(self.files[self.min_list - 1])["wavelength_axis"].tolist()
        light_level = pd.read_csv(self.files[self.min_list - 1])["light_level"].tolist()
        self.spectrum_analysis_ref, = self.ax1.plot(wavelength_axis, self.reference_light_level, label='reference', color='orange')
        self.spectrum_analysis, = self.ax1.plot(wavelength_axis, light_level, label='current', color='blue')
        self.subtracted_scan, = self.ax1_twin.plot(wavelength_axis, self.subtracted_light_level, label='subtracted scan', color='black')

    def plot_2(self):
        # set up plot of opm
        self.ax2_twin = self.ax2.twinx()
        self.ax2.ticklabel_format(useOffset=False)  # prevents scientific notation
        self.ax2_twin.ticklabel_format(useOffset=False)  # prevents scientific notation
        self.ax2_twin.set_ylabel("Spectrum Analyzer Power Level")
        self.ax2.set_ylabel("Power Meter Power Level")
        self.ax2.set_xlabel('Time')
        self.plot2, = self.ax2_twin.plot(self.opm_time, self.opm_reading, label='Power Meter Power Level', color='purple', marker="o")
        self.plot2_total_power, = self.ax2.plot(self.opm_time, self.total_power, label='SA Power Level', color='blue', marker="o")
        self.plot2_reference = self.ax2.axhline(y=self.reference_power_level, label='Reference SA Power Level', color='orange', linestyle='-')
        self.plot2_line = self.ax2.axvline(self.opm_time[self.min_list - 1], color='grey')
        self.ax2_twin.legend(bbox_to_anchor=(0, 1.3), loc='upper left')

    def plot_3(self):
        # set up plot for oven_data
        self.ax3.set_ylabel('Temperature (C)')
        self.ax3.set_xlabel('Time')
        self.plot3_cur, = self.ax3.plot(self.oven_time, self.cur_temp, label='Current Temp', color='Red', marker="o")
        self.plot3_setpoint, = self.ax3.plot(self.oven_time, self.setpoint_temp, label='Setpoint Temp', color='Green', marker="o")
        self.plot3_line = self.ax3.axvline(self.oven_time[self.min_list - 1], color='grey')
        # ax3.legend(bbox_to_anchor=(0, 1.18), loc='upper left')

    def plot_4(self):
        # setup plot for mean wavelength
        self.ax4.ticklabel_format(useOffset=False)  # prevents scientific notation
        self.ax4.set_ylabel('Mean Wavelength')
        self.ax4.set_xlabel('Time')
        self.plot4, = self.ax4.plot(self.oven_time, self.mean_wavelength, label='Mean Wavelength', color='Black', marker="o")
        self.plot4_reference = self.ax4.axhline(y=self.reference_mean_wavelength, color='orange', linestyle='-')
        self.plot4_line = self.ax4.axvline(self.oven_time[self.min_list - 1], color='grey')

    # animate the function
    def animate(self, i):
        # get data
        self.get_data(self.output_files_folder, self.final_csv_location)
        self.files = [f'{self.output_files_folder}/{name}' for name in os.listdir(self.output_files_folder)]
        # clear axis: This is necessary because we need to create new axis when there is new data
        self.ax2.cla()
        self.ax3.cla()
        self.ax4.cla()

        self.animate_spectrum_analyzer()
        self.animate_opm()
        self.animate_oven_data()
        self.animate_mean_wavelength()

        if self.event.is_set():
            self.event.clear()
            self.a.event_source.stop()
            print("Thread has exited")

    def animate_spectrum_analyzer(self):
        # animate spectrum analyzer
        self.ax1.set_xlim(self.minimum_index, self.maximum_index)
        self.ax1.set_ylim(-75, -25)
        self.slider.valinit = self.min_list
        self.slider.valmax = self.min_list
        self.slider.ax.set_xlim(1, self.min_list)
        self.slider.vline._linewidth = 0
        self.slider.reset()
        self.ax1.legend(bbox_to_anchor=(0, 1.18), loc='upper left')
        self.ax1_twin.legend(bbox_to_anchor=(0, 1.3), loc='upper left')

    def animate_opm(self):
        # animate opm
        self.ax2.set_ylabel('Power Meter Power Level')
        self.ax2.set_xlabel('Time (in hours)')
        self.ax2.ticklabel_format(useOffset=False)  # prevents scientific notation
        self.ax2_twin.ticklabel_format(useOffset=False)  # prevents scientific notation
        self.plot2, = self.ax2_twin.plot(self.opm_time, self.opm_reading, label='Power Meter Power Level', color='purple', marker="o")
        self.plot2_total_power, = self.ax2.plot(self.opm_time, self.total_power, label='SA Power Level', color='blue', marker="o")
        self.plot2_reference = self.ax2.axhline(y=self.reference_power_level, label='Reference SA Power Level', color='orange', linestyle='-')
        self.plot2_line = self.ax2.axvline(self.opm_time[self.min_list - 1], color='grey')
        self.ax2.legend(bbox_to_anchor=(0, 1.2), loc='upper left')

    def animate_oven_data(self):
        # animate oven_data
        self.ax3.set_ylabel('Temperature (C)')
        self.ax3.set_xlabel('Time (in hours)')
        self.plot3_cur, = self.ax3.plot(self.oven_time, self.cur_temp, label='Current Temp', color='Red', marker="o")
        self.plot3_setpoint, = self.ax3.plot(self.oven_time, self.setpoint_temp, label='Setpoint Temp', color='Green', marker="o")
        self.plot3_line = self.ax3.axvline(self.oven_time[self.min_list - 1], color='grey')
        self.ax3.legend(bbox_to_anchor=(0, 1.18), loc='upper left')

    def animate_mean_wavelength(self):
        # animate mean wavelength
        self.ax4.ticklabel_format(useOffset=False)  # prevents scientific notation
        self.ax4.set_ylabel('Mean Wavelength')
        self.ax4.set_xlabel('Time (in hours)')
        self.plot4, = self.ax4.plot(self.oven_time, self.mean_wavelength, label='Mean Wavelength', color='Black', marker="o")
        self.plot4_reference = self.ax4.axhline(y=self.reference_mean_wavelength, color='orange', linestyle='-')
        self.plot4_line = self.ax4.axvline(self.oven_time[self.min_list - 1], color='grey')

    # Call update function when slider value is changed
    def update(self, val):
        num = self.slider.val
        FILE = self.create_subtracted_data(num - 1)
        # update spectrum analyzer
        self.subtracted_scan.set_ydata(self.subtracted_light_level)
        self.spectrum_analysis_ref.set_ydata(self.reference_light_level)
        self.spectrum_analysis.set_xdata(FILE["wavelength_axis"].tolist())
        self.spectrum_analysis.set_ydata(FILE["light_level"].tolist())
        self.ax1.set_title(
            f"                                                        Date: {self.files[num - 1][-35:]}   Temperature: {self.cur_temp[num - 1]}   Power_Level: {self.opm_reading[num - 1]}")
        # update lines
        self.plot2_line.set_xdata(self.opm_time[num - 1])
        self.plot3_line.set_xdata(self.oven_time[num - 1])
        self.plot4_line.set_xdata(self.oven_time[num - 1])

    def create_subtracted_data(self, num=0):
        threshold = 30
        window = 30
        # create subtracted data
        FILE = pd.read_csv(self.files[num])
        self.subtracted_light_level = [element1 - element2 for (element1, element2) in zip(self.reference_light_level, FILE["light_level"].tolist())]

        for i in range(len(self.subtracted_light_level)):
            if abs(self.subtracted_light_level[i]) > threshold:
                if i == 0:
                    self.subtracted_light_level[i] = self.subtracted_light_level[i + 1]
                elif i == len(self.subtracted_light_level) - 1:
                    self.subtracted_light_level[i] = self.subtracted_light_level[i - 1]
                else:
                    self.subtracted_light_level[i] = (self.subtracted_light_level[i + 1] + self.subtracted_light_level[i - 1]) / 2  # average of neighbors

        for i in range(len(self.subtracted_light_level) - window):
            self.subtracted_light_level[i] = np.average(self.subtracted_light_level[i:(i + window)])
        for i in range(1, window + 1):
            self.subtracted_light_level[-i] = None
        return FILE

    def get_data(self, output_files_folder, final_output_location):
        # get data
        self.calculate_some_things(output_files_folder)
        final_output = pd.read_csv(final_output_location)
        opm_time = final_output["OpmTime"].tolist()
        opm_reading = final_output["OpmRead"].tolist()
        oven_time = final_output["OvenTime"].tolist()
        cur_temp = final_output["CurTemp"].tolist()
        setpoint_temp = final_output["SetpointTemp"].tolist()
        mean_wavelength_time = final_output["MeanWavelengthTime"].tolist()
        mean_wavelength = final_output["MeanWavelength"].tolist()
        self.total_power = final_output["sa_power_level"].tolist()
        self.min_list = min(self.number_of_files, len(opm_time), len(opm_reading), len(oven_time), len(cur_temp), len(setpoint_temp),
                            len(mean_wavelength_time), len(mean_wavelength))
        self.opm_time = opm_time[:self.min_list]
        self.opm_reading = opm_reading[:self.min_list]
        self.oven_time = oven_time[:self.min_list]
        self.cur_temp = cur_temp[:self.min_list]
        self.setpoint_temp = setpoint_temp[:self.min_list]
        self.mean_wavelength_time = mean_wavelength_time[:self.min_list]
        self.mean_wavelength = mean_wavelength[:self.min_list]

    def calculate_some_things(self, output_files_folder):
        """
        caluculates the mins and maxes as well as the number of files and files in the folder
        """
        self.files = [f'{output_files_folder}/{name}' for name in os.listdir(output_files_folder)]
        self.number_of_files = len(self.files)
        for num in range(1, self.number_of_files + 1):
            if num == 1:
                wavelength_axis = pd.read_csv(self.files[num - 1])["wavelength_axis"].tolist()
                light_level = pd.read_csv(self.files[num - 1])["light_level"].tolist()
                self.minimum_index = min(wavelength_axis)
                self.maximum_index = max(wavelength_axis)
                self.minimum_spectrum = min(light_level)
                self.maximum_spectrum = max(light_level)
            else:
                wavelength_axis = pd.read_csv(self.files[num - 1])["wavelength_axis"].tolist()
                light_level = pd.read_csv(self.files[num - 1])["light_level"].tolist()
                self.minimum_index = min(min(wavelength_axis), self.minimum_index)
                self.maximum_index = max(max(wavelength_axis), self.maximum_index)
                self.minimum_spectrum = min(min(light_level), self.minimum_spectrum)
                self.maximum_spectrum = max(max(light_level), self.maximum_spectrum)


if __name__ == '__main__':
    graph = SliderOldData(freq=1000, output_files_folder=r"C:\Users\ethan\Desktop\Spectrum Analyzer Test V3 - In Devlopment\V3 Testing\SA FILES",
                          final_csv_location=r"C:\Users\ethan\Desktop\Spectrum Analyzer Test V3 - In Devlopment\V3 Testing\FINAL CSV\final.csv",
                          reference_file_location=r"C:\Users\ethan\Desktop\Spectrum Analyzer Test V3 - In Devlopment\V3 Testing\REFERENCE FILES\00002__Wed Mar  2 18_07_35 2022_NORMHOLD.csv")
