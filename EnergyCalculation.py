#!/usr/bin/env python3
"""Module to process raw accelerometer files into readable data."""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import argparse


def main():
    """
    Application entry point responsible for parsing command line requests
    """
    parser = argparse.ArgumentParser(description='Process Non-wear-time accelerometer data.')
    parser.add_argument('input_file', metavar='file', type=str, nargs='+',
                        help='filename for csv accelerometer data')

    # parse command line arguments
    args = parser.parse_args()
    for file in args.input_file:
        energy_calculations(file)

def energy_calculations(input_file):
    """calculate energy and non-wear time stamps based on input file
                :param str input_file:  CSV from provided dataset
                :return: New file written to csv output naming convention and new png image of plot
                :rtype: void
    """
    df = pd.read_csv(input_file) # read data
    df['Time'] = pd.to_datetime(df['Time'], unit='ms') # convert timestamp to datetime object

    # save file name
    base_input_name = os.path.splitext(input_file)[0]

    # timestamp for filename
    now = datetime.datetime.now()
    timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))

    # Simple smoothing signal with rolling window
    # use rolling window of 10 samples ~ .5 second
    df['accX'] = df['accX'].rolling(window=10, min_periods=1).mean() # smoothing
    df['accY'] = df['accY'].rolling(window=10, min_periods=1).mean() # smoothing
    df['accZ'] = df['accZ'].rolling(window=10, min_periods=1).mean() # smoothing

    #rolling std
    df['stdX'] = df['accX'].rolling(300).std()*1000 # rolling std of 15 seconds is 300 samples
    df['stdY'] = df['accY'].rolling(300).std()*1000
    df['stdZ'] = df['accZ'].rolling(300).std()*1000 # 1000 X to convert g to mg

    # Calculate non-wear time using std if 2 of 3 axes is less than target, point can be marked as non-wear point
    target_std=13 # set target std to check against
    df["Non_Wear"] = (df['stdX'] < target_std) & (df['stdY'] < target_std) | (df['stdX'] < target_std) & (df['stdZ'] < target_std) | (df['stdY'] < target_std) & (df['stdZ'] < target_std)

    # Vector Mag to calc non-worn time
    df["Energy"]= np.sqrt((df['accX']**2) + (df['accY']**2) + (df['accZ']**2)) # energy calculation

    # plot the energy expenditure
    ax = df.plot(x="Time", y='Energy', rot=45, markersize=5)
    ax = plt.gca()

    # run gridlines for each hour bar
    ax.get_xaxis().grid(True, which='major', color='grey', alpha=0.5)
    ax.get_xaxis().grid(True, which='minor', color='grey', alpha=0.25)

    # mask the blocks for wear and non_wear time
    df['block'] = (df['Non_Wear'].astype(bool).shift() != df['Non_Wear'].astype(bool)).cumsum() # checks if next index label is different from previous
    df.assign(output=df.groupby(['block']).Time.apply(lambda x:x - x.iloc[0])) # calculate the time of each sample in blocks

    # times of blocks
    start_time_df = df.groupby(['block']).first() # start times of each blocked segment
    stop_time_df = df.groupby(['block']).last() # stop times for each blocked segment

    # lists of times stamps
    non_wear_starts_list=start_time_df[start_time_df['Non_Wear'] == True]['Time'].tolist()
    non_wear_stops_list=stop_time_df[stop_time_df['Non_Wear'] == True]['Time'].tolist()

    # new df from all non-wear periods
    data = { "Start": non_wear_starts_list, "Stop": non_wear_stops_list}
    df_non_wear=pd.DataFrame(data)
    df_non_wear['delta'] = [pd.Timedelta(x) for x in (df_non_wear["Stop"]) - pd.to_datetime(df_non_wear["Start"])]

    # check if non-wear is longer than target
    valid_no_wear = df_non_wear["delta"] > datetime.timedelta(minutes=5) #greater than 5 minutes
    no_wear_timestamps=df_non_wear[valid_no_wear]

    # list of valid non-wear starts and stops
    non_wear_start = no_wear_timestamps["Start"]
    non_wear_stop = no_wear_timestamps["Stop"]

    # plot non-wear periods
    ax.axvspan(non_wear_start, non_wear_stop, alpha=0.5, color='red')

    # save png image
    plt.savefig("non_wear_time_plot_" + base_input_name + "_" + timestamp + ".png", bbox_inches='tight')

    #show plot
    plt.title("Non-wear Time")
    plt.show()

if __name__ == '__main__':
    main()  # Standard boilerplate to call the main() function to begin the program.


