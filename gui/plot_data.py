#!/usr/bin/env python
# coding=utf-8

#==============================================================================
#
# Plot data from files %Y-%m-%d.txt and %Y-%m-%d_result.txt to file test.png
# By two variable raw_data_on and cal_data_on is possilbe to turn on/off 
# drawing raw data plot and calibrated data plot.
#
#==============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

#==============================================================================
# Open calibrated data
currtime    = datetime.datetime.now()
path = './' 
calb_data = path + currtime.strftime("%Y-%m-%d") + "_result.txt"

# Open data
currtime    = datetime.datetime.now()
path = './' 
raw_data = path + currtime.strftime("%Y-%m-%d") + ".txt"

#==============================================================================
# Create plot
fig, axes = plt.subplots(1, 3, figsize=(11, 3))
# axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
fontsize = 8
fig.suptitle('Raw and calibratedx10e3 data.', fontsize=fontsize)

# Set up fonts for all text objects
font = {'family' : 'normal',
        'size'   : 6}

matplotlib.rc('font', **font)

#==============================================================================
# Data processing

raw_data_on = True
cal_data_on = True

for data_num in range(3):
    # Calibrated data
    if cal_data_on:
        lines = open(calb_data, 'r').readlines()

        x_calb = np.linspace(0, len(lines), len(lines))
        y_calb = list()

        for line in lines:
            line = line[1:-2]
            y_calb.append(float(line.split(', ')[data_num])/10e7)
        # Add plot
        axes[data_num].plot(x_calb, y_calb, 'r')

    # Raw data
    if raw_data_on:
        lines = open(raw_data, 'r').readlines()

        x_raw = np.linspace(0, len(lines), len(lines))
        y_raw = list()

        for line in lines:
            line = line[1:-2]
            y_raw.append(float(line.split(', ')[data_num + 1])/10e7)
        # Add plot
        axes[data_num].plot(x_raw, y_raw, 'g')
            
    # Plot settings
    axes[data_num].grid(True)
    axes[data_num].set_xlabel('Iteration', fontsize=fontsize)
    axes[data_num].set_ylabel('Value [T]', fontsize=fontsize)

    for tick in axes[data_num].xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize) 
    for tick in axes[data_num].yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize) 
    # axes[data_num].set_title('title');

#==============================================================================

    axes[data_num].legend(['Calibrated data', 'Raw data'], loc=7, 
            prop={'size':fontsize})

#==============================================================================
# Save plot
#==============================================================================
plt.savefig("plot_1_calx1.png")
