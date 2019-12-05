"""Module to process raw accelerometer files into readable data."""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("acc_data.csv") # read data
df['Time'] = pd.to_datetime(df['Time'], unit='ms') # convert timestamp to seconds
df = df.set_index('Time') #index as timestamp to count
samples_seconds = df.resample('1S').count() # count sample in each 1s time period

samples_seconds["Reliability"]=samples_seconds['Hour']/20
samples_seconds.loc[samples_seconds['Reliability'] >= 1, 'Reliability'] = 1 #if sample rate greater than one set to 1
print(samples_seconds)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(samples_seconds)

# set and display plot
plot_df = samples_seconds.reset_index() # add index column in
print(plot_df)
ax = plot_df.plot(x="Time", y='Reliability', rot=45, style=".", markersize=5)
plt.show()