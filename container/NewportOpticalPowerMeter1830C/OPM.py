import pyvisa
import time
import csv
import os
from types import SimpleNamespace


def write_to_csv(Time, reading, number_of_runs):
    fieldnames = ["Time", "Reading"]
    if number_of_runs == 0:
        with open(os.path.join(os.getcwd(), "container/NewportOpticalPowerMeter1830C/optical_power_meter.csv"), 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            info = {
                "Time": Time,
                "Reading": reading
            }
            csv_writer.writerow(info)
    else:
        with open(os.path.join(os.getcwd(), "container/NewportOpticalPowerMeter1830C/optical_power_meter.csv"), 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": Time,
                "Reading": reading
            }
            csv_writer.writerow(info)


def optical_power_meter(**kwargs):
    kwarg = SimpleNamespace(**kwargs)
    connected = True
    previous_time = kwarg.original_time
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

    # Set up Top Multimeter
    try:
        OPM = rm.open_resource(kwarg.opm_port)  # this is the address of the Meter
        OPM.write("U3")                     # sets to dbm I think?
    except Exception:
        # In this case we don't have any connection to the power meter so None will just be written to the csv file
        print("Optical Power meter unable to connect! If you intended for this to be the case, everything is fine")
        connected = False

    number_of_runs = 0
    while True:
        if kwarg.e.is_set():
            time.sleep(10)
            print("optical power meter done")
            break
        if connected:
            # wait until the spectrum analyzer flag is set
            if kwarg.opm_flag.is_set():
                reading = OPM.query("D?")
                write_to_csv((time.time() - kwarg.original_time)/3600, reading, number_of_runs)
                number_of_runs = 1
                kwarg.opm_flag.clear()
        if not connected:
            if kwarg.opm_flag.is_set():
                reading = OPM.query("D?")
                write_to_csv((time.time() - kwarg.original_time)/3600, reading, number_of_runs)
                number_of_runs = 1
                kwarg.opm_flag.clear()


def main():
    from multiprocessing import Event
    optical_power_meter(opm_port='GPIB0::23::INSTR', freq=5, original_time=time.time(), e=Event())


if __name__ == '__main__':
    main()
