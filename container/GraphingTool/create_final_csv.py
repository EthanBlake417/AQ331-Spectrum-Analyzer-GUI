import pandas as pd


def create_final_csv(mean_wavelength_time, mean_wavelength, reference_mean_wavelength, oven_time, cur_temp, setpoint_temp, opm_time, opm_reading, sa_power_level, reference_power_level, final_csv_location):
    """ Creates the final csv with all the data nicely put together"""
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()
    df5 = pd.DataFrame()
    df["MeanWavelengthTime"] = mean_wavelength_time
    df["MeanWavelength"] = mean_wavelength
    df2["OvenTime"] = oven_time
    df2["CurTemp"] = cur_temp
    df2["SetpointTemp"] = setpoint_temp
    df3["OpmTime"] = opm_time
    df3["OpmRead"] = opm_reading
    df3["sa_power_level"] = sa_power_level
    df4["reference_mean_wavelength"] = [reference_mean_wavelength]
    df5['reference_power_level'] = [reference_power_level]

    new = pd.concat([df, df2, df3, df4, df5], axis=1)
    new.to_csv(final_csv_location, index=False)


def main():
    print("There is no way to test this apart from the whole system lol")


if __name__ == '__main__':
    main()
