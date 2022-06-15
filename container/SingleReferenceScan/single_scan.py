import pyvisa
import pandas as pd
import time
import os, os.path
import csv
import matplotlib.pyplot as plt
from types import SimpleNamespace
import tkinter
import math


def write_to_csv(Time, reading, number_of_runs):
    fieldnames = ["Time", "MeanWavelength"]
    if number_of_runs == 0:
        with open(os.path.join(os.getcwd(), "container/AQ6331SpectrumAnalyzer/mean_wavelength.csv"), 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            info = {
                "Time": Time,
                "MeanWavelength": reading
            }
            csv_writer.writerow(info)
    else:
        with open(os.path.join(os.getcwd(), "container/AQ6331SpectrumAnalyzer/mean_wavelength.csv"), 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": Time,
                "MeanWavelength": reading
            }
            csv_writer.writerow(info)


def spectrum_analyser(**kwargs):
    # Set up
    kwarg = SimpleNamespace(**kwargs)
    original_time = time.time()
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())
    spectrum_analyzer = rm.open_resource(kwarg.sa_port)  # this is the address of the Meter
    # print(spectrum_analyzer.query("*IDN?"))
    spectrum_analyzer.write("SD0")  # sets delimiter to ","
    # spectrum_analyzer.write("SEGP 7500")         # sets the number of samples in a sweep
    # spectrum_analyzer.write("REFLP" ANA?)
    spectrum_analyzer.write(f"CTRWL {kwarg.center_wavelength}")  # sets center wavelength
    spectrum_analyzer.write("LSUNT 0")  # 0: dBm(W) 1: dBm/nm(W/nm)
    spectrum_analyzer.write(f"RESLN {kwarg.resolution}")  # sets Resolution
    spectrum_analyzer.write(f"SPAN {kwarg.span}")  # sets span
    spectrum_analyzer.write(f"{kwarg.sensitivity}")
    spectrum_analyzer.write(f"SMPL{kwarg.sample_points}")
    number_of_runs = 0

    spectrum_analyzer.write("SGL")  # performs a single sweep
    # wait until sweep is done 1 means single sweep, 0 means stop
    while int(spectrum_analyzer.query("SWEEP?")):
        continue

    # get data
    l_data = spectrum_analyzer.query("LDATA")  # queries the light level in dbm(depends on settings)
    w_data = spectrum_analyzer.query("WDATA")  # queries the wavelength axis
    spectrum_analyzer.write("SW2")
    mean_wavelength = float(spectrum_analyzer.query("ANA?").split(",")[0])
    light_level = l_data.split(",")
    wavelength_axis = w_data.split(",")
    del (light_level[0])
    del (wavelength_axis[0])
    for i in range(len(wavelength_axis)):
        wavelength_axis[i] = float(wavelength_axis[i])
        light_level[i] = float(light_level[i])
    total_power = sum([(10 ** (val / 10)) for val in light_level])
    total_power = 10 * math.log10(total_power)
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df["wavelength_axis"] = wavelength_axis
    df["light_level"] = light_level
    df2["mean_wavelength"] = [mean_wavelength]
    df3["total_power"] = [total_power]
    write_to_csv((time.time() - original_time)/3600, mean_wavelength, number_of_runs)
    number_of_runs = 1
    new = pd.concat([df, df2, df3], axis=1)
    Time = str(time.ctime())
    Time = Time.replace(':', '_')

    # calculate min and max limits based on all the files.
    number_of_files = len([name for name in os.listdir(kwarg.output_files_folder)])
    zero_filled = str(number_of_files + 1).zfill(5)
    new.to_csv(f'{kwarg.output_files_folder}/{zero_filled}__{Time}__{kwarg.addendum}.csv', sep=',', index=False)

    # graph scan
    kwarg.ax.plot(wavelength_axis, light_level)
    kwarg.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # plt.show()
    kwarg.test_currently_running.clear()


def main():
    spectrum_analyser(sa_port='GPIB1::7::INSTR', output_files_folder=r'C:\Users\Work Computer\Desktop\Spectrum_Analyzer_Test\Reference CSV', resolution=str(1.00), center_wavelength=str(1310.00), span=str(120.0))


if __name__ == '__main__':
    main()
