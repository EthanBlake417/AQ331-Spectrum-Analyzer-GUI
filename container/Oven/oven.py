import csv
import time
from pywatlow.watlow import Watlow
import os
from types import SimpleNamespace


class EzZone:
    def __init__(self):
        self.original_time = None
        self.previous_write_time = None
        self.previous_inc_time = None
        self.watlow = None
        self.number_of_runs = 0

    @staticmethod
    def F_to_C(temp_in_fahrenheit):
        """Convert Fahrenheit to Celsius"""
        temp_in_celsius = (temp_in_fahrenheit - 32) * (5 / 9)
        return temp_in_celsius

    @staticmethod
    def C_to_F(temp_in_celsius):
        """Convert Celsius to Fahrenheit"""
        temp_in_fahrenheit = temp_in_celsius * (9 / 5) + 32
        return temp_in_fahrenheit

    def read(self):
        """ call this function to read the current temperature in the oven."""
        return round(self.F_to_C(self.watlow.read()['data']), 1)

    def read_setpoint(self):
        """ call this function to read the setpoint temperature in the oven."""
        return round(self.F_to_C(self.watlow.readSetpoint()['data']), 1)

    def write(self, temp_C):
        """ call this function to write a new temperature to the oven."""
        return self.watlow.write(round(self.C_to_F(temp_C), 1))

    def increment_temperature(self, increment):
        """ increments the setpoint temperature by the increment, most likely .1 degrees Celsius"""
        cur_setpoint = self.read_setpoint()
        self.write(cur_setpoint + increment)

    def write_to_csv(self):
        Time = (time.time() - self.original_time)/3600
        Real_Time = time.ctime()
        Current_temperature = self.read()
        Setpoint = self.read_setpoint()

        fieldnames = ["Real Time", "Time", "Current Temperature", "Setpoint"]
        if self.number_of_runs == 0:

            with open(os.path.join(os.getcwd(), "container/Oven/oven_data.csv"), 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                info = {
                    "Real Time": Real_Time,
                    "Time": Time,
                    "Current Temperature": Current_temperature,
                    "Setpoint": Setpoint
                }
                csv_writer.writerow(info)
            self.number_of_runs = 1
        else:
            with open(os.path.join(os.getcwd(), "container/Oven/oven_data.csv"), 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                info = {
                    "Real Time": Real_Time,
                    "Time": Time,
                    "Current Temperature": Current_temperature,
                    "Setpoint": Setpoint
                }
                csv_writer.writerow(info)

    def ramp_oven(self, setpoint, time_in_minutes, oven_flag):
        """ Ramp the oven to the desired temperature in a set amount of time."""
        # basic setup
        oven_ramping_state = "heating"
        time_in_seconds = time_in_minutes * 60
        increment = .1  # this is in degrees Celsius
        cur_setpoint = self.read_setpoint()  # the current setpoint of the oven

        # sleep if our new setpoint is same as what it previously was.
        if setpoint == cur_setpoint:
            while True:
                # wait until flag is set, then clear it after graphing
                if oven_flag.is_set():
                    self.write_to_csv()
                    oven_flag.clear()
                if time.time() - self.previous_inc_time >= time_in_seconds:
                    self.previous_inc_time += time_in_seconds
                    return

        # decrease or increase the temperature?
        if setpoint < cur_setpoint:  # decrease the temperature if cooling the oven
            oven_ramping_state = "cooling"
            increment = -increment

        # determine the wait_time between .1 degree increments
        difference = abs(
            setpoint - cur_setpoint) * 10  # the difference between the current temp and the new setpoint temp
        wait_time = time_in_seconds / difference  # How long to wait between each incrementation (in seconds)
        # keep incrementing until the setpoint is reached
        while True:
            if time.time() - self.previous_inc_time >= wait_time:
                self.previous_inc_time += wait_time
                self.increment_temperature(increment)
            # wait until flag is set, then clear it after graphing
            if oven_flag.is_set():
                self.write_to_csv()
                oven_flag.clear()
            if oven_ramping_state == "cooling" and setpoint >= self.read_setpoint():  # if we reach the setpoint, stop ramping the oven
                return
            elif oven_ramping_state == "heating" and setpoint <= self.read_setpoint():  # if we reach the setpoint, stop ramping the oven
                return

    def user_profile(self, **kwargs):
        """ Given a list of temperatures, and a list of times, the user profile runs the oven test."""
        kwarg = SimpleNamespace(**kwargs)
        self.original_time = kwarg.original_time
        self.previous_write_time = kwarg.original_time
        self.previous_inc_time = kwarg.original_time
        self.watlow = Watlow(port=kwarg.oven_port, address=1)
        for i in range(len(kwarg.list_of_temperatures)):
            self.ramp_oven(kwarg.list_of_temperatures[i], kwarg.list_of_times[i], kwarg.oven_flag)
        print("Oven profile is completed")
        kwarg.e.set()                       # this should
        return


def main():
    """ Test different user profiles. All temperatures should be in celsius, and the time is in minutes.
    Increment is assumed to be .1 degrees Celsius"""
    # this is a basic user profile.
    ez = EzZone()
    ez.user_profile(port="COM4", list_of_temperatures=[24, 27, 27, 30, 26, 26], list_of_times=[0, .5, .2, .4, .1, .5], on_off_time=10, original_time=time.time())


if __name__ == '__main__':
    main()
