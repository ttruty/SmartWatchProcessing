#!/usr/bin/env python3
"""Module to process raw accelerometer files into readable data."""
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import argparse
import os


def main():
    """
    Application entry point responsible for parsing command line requests
    """
    parser = argparse.ArgumentParser(description='Process accelerometer data.')
    parser.add_argument('input_file', metavar='file', type=str, nargs='+',
                        help='filename for csv accelerometer data')

    # parse command line arguments
    args = parser.parse_args()
    for file in args.input_file:
        reliability_score(file)


def reliability_score(input_file):
    """ calculate reliability score based on input file
            :param str input_file:  CSV from provided dataset
            :return: New file written to csv output naming convention and new png image of plot
            :rtype: void
    """
    sampling_rate=20 # Sample rate (Hz) for target device data

    # save file name
    base_input_name = os.path.splitext(input_file)[0]

    # timestamp for filename
    now = datetime.datetime.now()
    timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))

    df = pd.read_csv(input_file) # read data

    df['Time'] = pd.to_datetime(df['Time'], unit='ms') # convert timestamp to seconds
    df = df.set_index('Time') #index as timestamp to count
    samples_seconds = df.resample('1S').count() # count sample in each 1s time period

    # reliability by second
    samples_seconds['Reliability']= samples_seconds['Hour'] / sampling_rate
    samples_seconds.loc[samples_seconds['Reliability'] >= 1, 'Reliability'] = 1 #if sample rate greater than one set to 1

    # save csv of reliability by second
    header = ["Reliability"]
    samples_seconds.to_csv("reliability_csv_by_seconds_" + base_input_name + "_" + timestamp + ".csv" , columns=header)

    print("Reliability for data set = " + str(samples_seconds["Reliability"].mean(axis=0)))

    # set and display plot
    plot_df = samples_seconds.reset_index() # add index column
    plot_df.plot(x='Time', y='Reliability', rot=45, style=".", markersize=5)

    # save png image
    plt.savefig("reliability_plot_" + base_input_name + "_" + timestamp + ".png", bbox_inches='tight')

    #show plot
    plt.title("Reliability Score by Second")
    plt.show()

if __name__ == '__main__':
    main()  # Standard boilerplate to call the main() function to begin the program.

