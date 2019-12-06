#!/usr/bin/env python3
"""Combine all hours of data into one CSV"""
import pandas as pd

#output combined CSV file
def concat_file(file_list, output_file):
    """concat .csv file according to list of files
        :param str file_list: List of  CSV from provided dataset
        :param str output_file: Output filename to save the concat CSV of files
        :return: New file written to <output_file>
        :rtype: void
    """
    combined_csv = pd.concat([pd.read_csv(f) for f in file_list ]) #combine all files in the list
    combined_csv.to_csv( output_file, index=False, encoding='utf-8-sig') #export to csv with uft-8 encoding

# hold paths for each hour
acc_file_locations=[]
gyro_file_locations=[]

# loop to add path hours to list
for hour in range (12,18):
    acc_file_locations.append("Data-raw/Accelerometer/2019-11-12/" + str(hour) + "/accel_data.csv")
    gyro_file_locations.append("Data-raw/Gyroscope/2019-11-12/" + str(hour) + "/accel_data.csv")

concat_file(acc_file_locations, 'acc_data.csv')
concat_file(gyro_file_locations, 'gyro_data.csv')