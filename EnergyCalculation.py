"""Module to process raw accelerometer files into readable data."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("acc_data.csv") # read data
df['Time'] = pd.to_datetime(df['Time'], unit='ms') # convert timestamp to seconds
# df = df.set_index('Time') #index as timestamp to count
# samples_seconds = df.resample('1S').count() # count sample in each 1s time period

df["Energy"]= np.sqrt((df['accX']**2) + (df['accY']**2) + (df['accZ']**2)) # energy calculation
print(df)
#df["Wearing"].loc[df['Energy'] <5 , 'Reliability'] = 1 #if sample rate greater than one set to 1
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)
ax = df.plot(x="Time", y='Energy', rot=45, markersize=5)
ax = plt.gca()
# run gridlines for each hour bar
ax.get_xaxis().grid(True, which='major', color='grey', alpha=0.5)
ax.get_xaxis().grid(True, which='minor', color='grey', alpha=0.25)


plt.show()
non_wear = df[df["Energy"] < 5]
print(non_wear)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(non_wear)
