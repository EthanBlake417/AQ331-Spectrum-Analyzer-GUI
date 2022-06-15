import pyvisa
import pandas as pd
import time
import os, os.path
import csv
import math
from types import SimpleNamespace


def write_to_csv(Time, reading, total_power, number_of_runs):
    fieldnames = ["Time", "MeanWavelength", "TotalPower"]
    if number_of_runs == 0:
        with open(os.path.join(os.getcwd(), "container/AQ6331SpectrumAnalyzer/mean_wavelength.csv"), 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            info = {
                "Time": Time,
                "MeanWavelength": reading,
                "TotalPower": total_power
            }
            csv_writer.writerow(info)
    else:
        with open(os.path.join(os.getcwd(), "container/AQ6331SpectrumAnalyzer/mean_wavelength.csv"), 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": Time,
                "MeanWavelength": reading,
                "TotalPower": total_power
            }
            csv_writer.writerow(info)


def spectrum_analyser(**kwargs):
    # change it so I can use dot format using SimpleNameSpace
    kwarg = SimpleNamespace(**kwargs)
    # Set up
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
    previous_time = kwarg.original_time - kwarg.freq
    number_of_runs = 0

    # I'm thinking, set a flag for each process right after starting the sweep, and have each process wait for that flag and run, and shut the flag off.
    while True:
        if kwarg.e.is_set():
            time.sleep(10)
            print("spectrum analyzer done")
            break
        if time.time() - previous_time >= kwarg.freq:
            previous_time = previous_time + kwarg.freq
            spectrum_analyzer.write("SGL")  # performs a single sweep
            # set flags
            kwarg.oven_flag.set()
            kwarg.opm_flag.set()
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
            df["wavelength_axis"] = wavelength_axis
            df["light_level"] = light_level
            write_to_csv((time.time() - kwarg.original_time) / 3600, mean_wavelength, total_power, number_of_runs)
            number_of_runs = 1
            new = pd.concat([df], axis=1)
            Time = str(time.ctime())
            Time = Time.replace(':', '_')

            # calculate min and max limits based on all the files.
            number_of_files = len([name for name in os.listdir(kwarg.output_files_folder)])
            zero_filled = str(number_of_files + 1).zfill(5)
            new.to_csv(f'{kwarg.output_files_folder}/{zero_filled}__{Time}.csv', sep=',', index=False)
            kwarg.ready_to_graph_flag.set()


def main():
    from multiprocessing import Event
    spectrum_analyser(sa_port='GPIB1::7::INSTR', freq=1, output_files_folder=None, original_time=time.time(), e=Event(), resolution=str(1.00), center_wavelength=str(1310.00), span=str(120.0), sensitivity="SNHD", sample_points="4000")


if __name__ == '__main__':
    main()
