# One problem that I was running into is that the code just stops working for a few minutes at a time. I was trying to figure
    # out why this was happening so I could fix it. Look at Hyrum Taylor's research notebook June 23 - July 1 for how to record
    # system data.
# Once the system data is recorded along with a time gap in the stabilization code, I can use this code to plot and see how system
    # resources are related to the time gaps. Spoiler, on July 1, I found that the processor time is spiking signficnatly, 
    # but I'm not sure how to fix it.
# However, as long as the computer isn't doing anything else super strenuous (like waking up after a restart), time gaps don't
    # happen, so unless it really starts being a problem, I'm not worried about this for now.

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import datetime

csv_name = "2025-06-26 13-33-54_stabilized.csv"
ram_tsv = "logfile13.tsv"


csv_file_path = os.path.join(os.getcwd(),'CSV',csv_name)
arr1 = []
arr2 = []
with open(csv_file_path, 'r') as f:
    data = csv.reader(f)
    next(data) # first line is column description, not data
    for line in data:
        if (line[0] != ""): # If one array was longer than the other, filled in time steps with None
            arr1.append(line[:6])
        if (line[4] != ""):
            arr2.append(line[6:])
    arr1 = np.array(arr1).astype(float) # "time_steps1","y_cam_err1","x_cam_err1","tot_cam_err1","y_mot_steps1","x_mot_steps1"
    arr2 = np.array(arr2).astype(float) # "time_steps2","y_cam_err2","x_cam_err2","tot_cam_err2","y_mot_steps2","x_mot_steps2"


tsv_file_path = os.path.join(os.getcwd(),'CSV','Python Resource Logs','log_file_tsvs',ram_tsv)
ram_arr = []
with open(tsv_file_path, 'r') as f:
    data = csv.reader(f,delimiter='\t')
    next(data) # first line is column description, not data
    for line in data:
        timestamp = datetime.datetime.strptime(line[0],'%m/%d/%Y %H:%M:%S.%f').timestamp()
        if str.strip(line[1]) == '':
            line[1] = 0
        if str.strip(line[2]) == '':
            line[2] = 0
        ram_arr.append([timestamp,line[1],line[2]])
    ram_arr = np.array(ram_arr).astype(float) # time, processor usage, free ram
ram_arr[:,2] = ram_arr[:,2]*10**-6 # convert bytes -> MB

# --- Now that I have the data pulled out of the file, I can make graphs with it! (first index is time, second is data type)
#           ["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]


tstart = min(min(arr1[0,0],arr2[0,0]), ram_arr[0,0]) # used to scale the time axis on the graphs so it's equal on both
tend = max(max(arr1[-1,0],arr2[-1,0]), ram_arr[-1,0])
time_elapsed = tend - tstart
arr1[:,0] -= tstart
arr2[:,0] -= tstart
ram_arr[:,0] -= tstart


if True:  # This graph shows camera error vs motor steps over time
    plot_y_axis = True   # if set to false, it plots x axis instead

    ind_t = 0 # index for time steps, same for arr1 and arr2

    ind_c = 1 # index for camera Y-axis, same for arr1 and arr2
    ind_m = 4 # index for motor Y-axis, same for arr1 and arr2s
    axis = "Y"

    if plot_y_axis == False:
        ind_c = 2 # index for camera X-axis, same for arr1 and arr2
        ind_m = 5 # index for motor X-axis, same for arr1 and arr2
        axis = "X"

    fig, ax = plt.subplots(2,1, figsize=(8,6))
    plt.suptitle(csv_name + " - steps vs. free RAM for " + axis + " axis" , fontweight="bold")

    tstart = min(arr1[0,0], arr2[0,0])

    left_time = .2*time_elapsed  # used to set the edges of the graph: default it -.03 -> 1.03 * time_elapsed
    right_time = .45*time_elapsed    # Can be used to focus in on a time region

    ax[0].plot(arr1[:,ind_t], arr1[:,ind_c],'.-b', label="Pixel Error 1")
    ax[0].plot(arr2[:,ind_t], arr2[:,ind_c],'.-r', label="Pixel Error 2")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[0].set_title("Camera error in pixels")
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Pixels")
    ax[0].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[0].set_xlim(left_time, right_time) # make graphs have same (asethetic) time length
    #ax[0].set_ylim(-1.5,1.5)
    ax[0].axhline(0, color="black", linewidth=.5)

    green = 'tab:green'
    purple = 'tab:purple'

    ax[1].plot(ram_arr[:,0], ram_arr[:,1],'.-', color=green, label="% CPU usage")    
    ax[1].set_ylabel("% Processor Time", color=green)
    ax[1].set_xlim(left_time, right_time)
    ax[1].set_ylim(np.min(ram_arr[:,1]), np.max(ram_arr[:,1]))
    ax[1].tick_params(axis='y', labelcolor=green)

    ax12 = ax[1].twinx()

    ax12.plot(ram_arr[:,0], ram_arr[:,2],'.-', color=purple, label="RAM usage")
    ax12.set_ylim(np.min(ram_arr[:,2]), np.max(ram_arr[:,2]))
    ax12.set_ylabel("Memory (MB)", color=purple)
    ax12.tick_params(axis='y', labelcolor=purple)

    ax[1].legend(loc="lower left")#, fancybox=True, framealpha=1)
    ax12.legend(loc="lower right")#, fancybox=True, framealpha=1)
    ax[1].set_title("Amount of used memory, processor usage over time")
    ax[1].axhline(0, color="black", linewidth=.5)
    ax[1].set_xlabel("Time")

    plt.tight_layout()
    plt.show()